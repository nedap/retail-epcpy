import re
from enum import Enum

from base_scheme import EPC_SCHEME
from common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    base64_to_hex,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    decode_string,
    encode_partition_table,
    encode_string,
    hex_to_binary,
    replace_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from regex import SGTIN_URI

SGTIN_PREFIX = "urn:epc:id:sgtin:"
COMPANY_PREFIX_REGEX = "\d+"
ITEM_REFERENCE_REGEX = "\d+"
SERIAL_REGEX = ".+"

SGTIN_REGEX = re.compile(SGTIN_URI)

SGTIN_PAT_PREFIX = "urn:epc:idpat:sgtin:"
SGTIN_PAT_REGEX = re.compile(
    f"^{SGTIN_PAT_PREFIX}((\d+\.\d+\..+)|(\d+\.\d+\.\*)|(\d+\.\*\.\*)|(\*\.\*\.\*))$"
)

TAG_URI_SGTIN_REGEX = re.compile("^urn:epc:tag:(sgtin-96|sgtin-198):\d.\d+\.\d+\..+$")
GTIN_CONVERTABLE_URIS_REGEX = re.compile(
    f"^({SGTIN_PREFIX}{COMPANY_PREFIX_REGEX}\.{ITEM_REFERENCE_REGEX}\.{SERIAL_REGEX})|({SGTIN_PAT_PREFIX}((\d+\.\d+\..+)|(\d+\.\d+\.\*)))$"
)

PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 4,
        "K": 1,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 7,
        "K": 2,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 10,
        "K": 3,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 14,
        "K": 4,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 17,
        "K": 5,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 20,
        "K": 6,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 24,
        "K": 7,
    },
}

PARTITION_TABLE_L = {
    12: PARTITION_TABLE_P[0],
    11: PARTITION_TABLE_P[1],
    10: PARTITION_TABLE_P[2],
    9: PARTITION_TABLE_P[3],
    8: PARTITION_TABLE_P[4],
    7: PARTITION_TABLE_P[5],
    6: PARTITION_TABLE_P[6],
}
# TODO: GTIN 8/12/13


class SGTINFilterValues(Enum):
    ALL_OTHERS = "0"
    POS_ITEM = "1"
    FULL_CASE = "2"
    RESERVED_3 = "3"
    INNER_PACK = "4"
    RESERVED_5 = "5"
    UNIT_LOAD = "6"
    COMPONENT = "7"


class SGTIN(EPC_SCHEME):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SGTIN_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        if len("".join(epc_uri.split(":")[4].split(".")[:2])) != 13:
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | Company prefix + item reference must be 13 digits"
            )

        serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(serial)

        self.epc_uri = epc_uri

        self._gtin = None

    def gs1_element_string(self) -> str:
        gtin = self.gtin()
        serial = replace_uri_escapes(".".join(self.epc_uri.split(".")[2:]))

        return f"(01){gtin}(21){serial}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes, filter_value: SGTINFilterValues
    ) -> str:
        if self._tag_uri:
            return self._tag_uri

        if binary_coding_scheme is None or filter_value is None:
            raise ConvertException(
                message="Both a binary coding scheme and a filter value should be provided!"
            )

        scheme = binary_coding_scheme.value
        filter_val = filter_value.value
        value = ":".join(self.epc_uri.split(":")[4:])
        serial = ".".join(value.split(".")[2:])

        if (
            scheme == BinaryCodingSchemes.SGTIN_198.value
            and len(replace_uri_escapes(serial)) > 20
        ) or (
            scheme == BinaryCodingSchemes.SGTIN_96.value
            and (
                not serial.isnumeric()
                or int(serial) >= pow(2, 38)
                or (len(serial) > 1 and serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {serial}")

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{value}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingSchemes = None,
        filter_value: SGTINFilterValues = None,
    ) -> str:
        if self._binary:
            return self._binary

        self.tag_uri(binary_coding_scheme, filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        gtin = self._tag_uri.split(":")[4].split(".")[1:3]
        serial = ".".join(self._tag_uri.split(".")[3:])

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        gtin_binary = encode_partition_table(gtin, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(serial, 38)
            if scheme == "SGTIN_96"
            else encode_string(serial, 140)
        )

        _binary = header + filter_binary + gtin_binary + serial_binary
        return _binary

    def gtin(self) -> str:
        if self._gtin:
            return self._gtin

        value = self.epc_uri.split(":")[4]

        company_pref = value.split(".")[0]
        indicator = value.split(".")[1][0]
        item_ref = value.split(".")[1][1:]
        digits = (indicator + company_pref + item_ref).zfill(13)
        checksum = calculate_checksum(digits)

        self._gtin = f"{digits}{checksum}"
        return self._gtin


def sgtin_to_gtin(sgtin: str) -> str:
    if not GTIN_CONVERTABLE_URIS_REGEX.match(sgtin):
        raise ConvertException(message=f"Invalid SGTIN {sgtin}")

    value = sgtin.split(":")[4]

    company_pref = value.split(".")[0]
    indicator = value.split(".")[1][0]
    item_ref = value.split(".")[1][1:]
    digits = (indicator + company_pref + item_ref).zfill(13)
    checksum = calculate_checksum(digits)

    return f"{digits}{checksum}"


def sgtin_to_gs1_element_string(sgtin: str) -> str:
    gtin = sgtin_to_gtin(sgtin)
    serial = replace_uri_escapes(sgtin.split(".")[-1])

    return f"(01){gtin}(21){serial}"


def binary_to_value_sgtin96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    gtin_binary = truncated_binary[11:58]
    serial_binary = truncated_binary[58:]

    filter_string = binary_to_int(filter_binary)
    gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)
    serial_string = binary_to_int(serial_binary)

    return f"{filter_string}.{gtin_string}.{serial_string}"


def binary_to_value_sgtin198(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    gtin_binary = truncated_binary[11:58]
    serial_binary = truncated_binary[58:]

    filter_string = binary_to_int(filter_binary)
    gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)
    serial_string = decode_string(serial_binary)

    return f"{filter_string}.{gtin_string}.{serial_string}"


def tag_to_value_sgtin96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])


def tag_to_value_sgtin198(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])


def binary_to_gtin14(binary: str) -> str:
    header = binary[:8]
    try:
        scheme = BinaryHeaders(header).name.replace("_", "-").lower()
    except ValueError:
        raise ConvertException(message=f"{header} is not a valid header")

    size = int(scheme.split("-")[-1])

    if not size <= len(binary):
        raise ConvertException(
            message=f"Invalid binary size, expected (<=): {size} actual: {len(binary)}"
        )

    truncated_binary = binary[:size]

    gtin_binary = truncated_binary[11:58]
    gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)

    return sgtin_to_gtin(f"urn:epc:id:sgtin:{gtin_string}.*")


def hex_to_gtin14(hex_string: str) -> str:
    binary = hex_to_binary(hex_string)

    return binary_to_gtin14(binary)


def base64_to_gtin14(base64_string: str) -> str:
    hex_string = base64_to_hex(base64_string)

    return hex_to_gtin14(hex_string)
