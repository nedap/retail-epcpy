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
    encode_partition_table,
    str_to_binary,
)
from regex import GSRN_URI

GSRN_URI_REGEX = re.compile(GSRN_URI)


PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 18,
        "K": 5,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 21,
        "K": 6,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 24,
        "K": 7,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 28,
        "K": 8,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 31,
        "K": 9,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 34,
        "K": 10,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 38,
        "K": 11,
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


class GSRNFilterValues(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GSRN(EPC_SCHEME):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GSRN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        if len(epc_uri.split(":")[4].replace(".", "")) != 17:
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | wrong number of digits"
            )

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        company_prefix, service_reference = self.epc_uri.split(":")[4].split(".")
        check_digit = calculate_checksum(f"{company_prefix}{service_reference}")

        return f"(8018){company_prefix}{service_reference}{check_digit}"

    def tag_uri(self, filter_value: GSRNFilterValues) -> str:
        if self._tag_uri:
            return self._tag_uri

        if filter_value is None:
            raise ConvertException(
                message="Either tag_uri should be set or a filter value should be provided"
            )

        scheme = BinaryCodingSchemes.GSRN_96.value
        filter_val = filter_value.value
        value = self.epc_uri.split(":")[4]

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{value}"

        return self._tag_uri

    def binary(self, filter_value: GSRNFilterValues = None) -> str:
        if self._binary:
            return self._binary

        self.tag_uri(filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        gsrn = self._tag_uri.split(":")[4].split(".")[1:]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        gsrn_binary = encode_partition_table(gsrn, PARTITION_TABLE_L)

        self._binary = header + filter_binary + gsrn_binary + "0" * 24
        return self._binary


def binary_to_value_gsrn96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    gsrn_binary = truncated_binary[11:72]

    filter_string = binary_to_int(filter_binary)
    gsrn_string = decode_partition_table(gsrn_binary, PARTITION_TABLE_P)

    return f"{filter_string}.{gsrn_string}"


def tag_to_value_gsrn96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
