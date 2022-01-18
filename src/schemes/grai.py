import re
from enum import Enum

from base_scheme import EPC_SCHEME
from common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    decode_string,
    encode_partition_table,
    encode_string,
    replace_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from regex import GRAI_URI

GRAI_URI_REGEX = re.compile(GRAI_URI)

PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 4,
        "K": 0,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 7,
        "K": 1,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 10,
        "K": 2,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 14,
        "K": 3,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 17,
        "K": 4,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 20,
        "K": 5,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 24,
        "K": 6,
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


class GRAIFilterValues(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GRAI(EPC_SCHEME):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GRAI_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        if len("".join(epc_uri.split(":")[4].split(".")[:2])) != 12:
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | Company prefix + asset type must be 12 digits"
            )

        serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(serial)

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        company_prefix, asset_type, *serial = ":".join(
            self.epc_uri.split(":")[4:]
        ).split(".")
        check_digit = calculate_checksum(f"{company_prefix}{asset_type}")

        serial = replace_uri_escapes(".".join(serial))

        return f"(8003)0{company_prefix}{asset_type}{check_digit}{serial}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes, filter_value: GRAIFilterValues
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
            scheme == BinaryCodingSchemes.GRAI_170.value
            and len(replace_uri_escapes(serial)) > 20
        ) or (
            scheme == BinaryCodingSchemes.GRAI_96.value
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
        filter_value: GRAIFilterValues = None,
    ) -> str:
        if self._binary:
            return self._binary

        self.tag_uri(binary_coding_scheme, filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        grai = self._tag_uri.split(":")[4].split(".")[1:3]
        serial = ".".join(self._tag_uri.split(".")[3:])

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        grai_binary = encode_partition_table(grai, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(serial, 38)
            if scheme == "GRAI_96"
            else encode_string(serial, 112)
        )

        _binary = header + filter_binary + grai_binary + serial_binary
        return _binary


def binary_to_value_grai96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    grai_binary = truncated_binary[11:58]
    serial_binary = truncated_binary[58:]

    filter_string = binary_to_int(filter_binary)
    grai_string = decode_partition_table(grai_binary, PARTITION_TABLE_P)
    serial_string = binary_to_int(serial_binary)

    return f"{filter_string}.{grai_string}.{serial_string}"


def binary_to_value_grai170(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    grai_binary = truncated_binary[11:58]
    serial_binary = truncated_binary[58:]

    filter_string = binary_to_int(filter_binary)
    grai_string = decode_partition_table(grai_binary, PARTITION_TABLE_P)
    serial_string = decode_string(serial_binary)

    return f"{filter_string}.{grai_string}.{serial_string}"


def tag_to_value_grai96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])


def tag_to_value_grai170(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
