import re
from enum import Enum

from base_scheme import EPCScheme
from common import (
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
from regex import SGCN_URI

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


class SGCN(EPCScheme):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SGCN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        company_prefix, coupon_ref, serial = epc_uri.split(":")[4].split(".")

        if len(f"{company_prefix}{coupon_ref}") != 12 or len(serial) > 12:
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | wrong number of digits"
            )

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        company_prefix, coupon_ref, serial = self.epc_uri.split(":")[4].split(".")
        check_digit = calculate_checksum(f"{company_prefix}{coupon_ref}")

        return f"(255){company_prefix}{coupon_ref}{check_digit}{serial}"

    def tag_uri(self, filter_value: SGCNFilterValues) -> str:
        if self._tag_uri:
            return self._tag_uri

        if filter_value is None:
            raise ConvertException(
                message="Either tag_uri should be set or a filter value should be provided"
            )

        scheme = BinaryCodingSchemes.SGCN_96.value
        filter_val = filter_value.value
        value = self.epc_uri.split(":")[4]

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{value}"

        return self._tag_uri

    def binary(self, filter_value: SGCNFilterValues = None) -> str:
        if self._binary:
            return self._binary

        self.tag_uri(filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        sgcn = self._tag_uri.split(":")[4].split(".")[1:3]
        serial = self._tag_uri.split(":")[4].split(".")[3]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        sgcn_binary = encode_partition_table(sgcn, PARTITION_TABLE_L)
        serial_binary = encode_numeric_string(serial, 41)

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
