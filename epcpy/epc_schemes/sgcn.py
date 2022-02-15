import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_numeric_string,
    decode_partition_table,
    encode_numeric_string,
    encode_partition_table,
    str_to_binary,
)
from epcpy.utils.regex import SGCN_URI

SGCN_URI_REGEX = re.compile(SGCN_URI)


PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 1,
        "K": 0,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 4,
        "K": 1,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 7,
        "K": 2,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 11,
        "K": 3,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 14,
        "K": 4,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 17,
        "K": 5,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 21,
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


class SGCNFilterValues(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class SGCN(EPCScheme, TagEncodable, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SGCN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid SGCN URI {epc_uri}")

        self._company_pref, self._coupon_ref, self._serial = epc_uri.split(":")[
            4
        ].split(".")

        if (
            len(f"{self._company_pref}{self._coupon_ref}") != 12
            or len(self._serial) > 12
            or not (6 <= len(self._company_pref) <= 12)
        ):
            raise ConvertException(
                message=f"Invalid SGCN URI {epc_uri} | wrong number of digits"
            )

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._coupon_ref}")
        self._gcn = f"{self._company_pref}{self._coupon_ref}{check_digit}{self._serial}"

    def gs1_key(self) -> str:
        return self._gcn

    def gs1_element_string(self) -> str:
        return f"(255){self._gcn}"

    def tag_uri(self, filter_value: SGCNFilterValues) -> str:
        if filter_value is None and self._tag_uri is None:
            raise ConvertException(
                message="Either tag_uri should be set or a filter value should be provided"
            )
        elif self._tag_uri:
            return self._tag_uri

        scheme = BinaryCodingSchemes.SGCN_96.value
        filter_val = filter_value.value

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._coupon_ref}.{self._serial}"

        return self._tag_uri

    def binary(self, filter_value: SGCNFilterValues = None) -> str:
        if filter_value is None and self._binary:
            return self._binary

        self.tag_uri(filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._coupon_ref]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        sgcn_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = encode_numeric_string(self._serial, 41)

        self._binary = header + filter_binary + sgcn_binary + serial_binary
        return self._binary


def binary_to_value_sgcn96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    sgcn_binary = truncated_binary[11:55]
    serial_binary = truncated_binary[55:]

    filter_string = binary_to_int(filter_binary)
    sgcn_string = decode_partition_table(sgcn_binary, PARTITION_TABLE_P)
    serial_string = decode_numeric_string(serial_binary)

    return f"{filter_string}.{sgcn_string}.{serial_string}"


def tag_to_value_sgcn96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
