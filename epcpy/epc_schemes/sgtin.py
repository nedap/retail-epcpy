import re
from enum import Enum, IntEnum

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
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
from epcpy.utils.regex import SGTIN_URI

SGTIN_REGEX = re.compile(SGTIN_URI)

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


class SGTINFilterValues(Enum):
    ALL_OTHERS = "0"
    POS_ITEM = "1"
    FULL_CASE = "2"
    RESERVED_3 = "3"
    INNER_PACK = "4"
    RESERVED_5 = "5"
    UNIT_LOAD = "6"
    COMPONENT = "7"


class GTIN_TYPE(IntEnum):
    GTIN8 = (8,)
    GTIN12 = (12,)
    GTIN13 = (13,)
    GTIN14 = 14


class SGTIN(EPCScheme, TagEncodable, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SGTIN_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid SGTIN URI {epc_uri}")

        if len("".join(epc_uri.split(":")[4].split(".")[:2])) != 13:
            raise ConvertException(
                message=f"Invalid SGTIN URI {epc_uri} | Company prefix + item reference must be 13 digits"
            )

        serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(serial)

        self.epc_uri = epc_uri

        value = self.epc_uri.split(":")[4]
        self._company_pref = value.split(".")[0]
        self._item_ref = value.split(".")[1]
        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )

        self._serial = serial
        self._gtin = f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}".zfill(
            14
        )

    def gs1_key(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        return self.gtin(gtin_type=gtin_type)

    def gtin(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        if gtin_type != GTIN_TYPE.GTIN14:
            if not self._gtin.startswith((14 - gtin_type) * "0"):
                raise ConvertException(message=f"Invalid GTIN{gtin_type}")

        return self._gtin[14 - gtin_type : 14]

    def gs1_element_string(self) -> str:
        gtin = self._gtin
        serial = replace_uri_escapes(self._serial)

        return f"(01){gtin}(21){serial}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes, filter_value: SGTINFilterValues
    ) -> str:
        if (
            binary_coding_scheme is None or filter_value is None
        ) and self._tag_uri is None:
            raise ConvertException(
                message="Either both a binary coding scheme and a filter value should be provided, or tag_uri should be set."
            )
        elif self._tag_uri:
            return self._tag_uri

        scheme = binary_coding_scheme.value
        filter_val = filter_value.value

        if (
            scheme == BinaryCodingSchemes.SGTIN_198.value
            and len(replace_uri_escapes(self._serial)) > 20
        ) or (
            scheme == BinaryCodingSchemes.SGTIN_96.value
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 38)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._item_ref}.{self._serial}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingSchemes = None,
        filter_value: SGTINFilterValues = None,
    ) -> str:
        if (binary_coding_scheme is None or filter_value is None) and self._binary:
            return self._binary

        self.tag_uri(binary_coding_scheme, filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._item_ref]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        gtin_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(self._serial, 38)
            if scheme == "SGTIN_96"
            else encode_string(self._serial, 140)
        )

        _binary = header + filter_binary + gtin_binary + serial_binary
        return _binary


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
