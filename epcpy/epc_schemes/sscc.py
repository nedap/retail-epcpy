from __future__ import annotations
import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    encode_partition_table,
    parse_header_and_truncate_binary,
    str_to_binary,
)
from epcpy.utils.regex import SSCC_URI

SSCC_URI_REGEX = re.compile(SSCC_URI)


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


class SSCCFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    FULL_CASE = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    UNIT_LOAD = "6"
    RESERVED_7 = "7"


class SSCC(EPCScheme, TagEncodable, GS1Keyed):
    class BinaryCodingScheme(Enum):
        SSCC_96 = "sscc-96"

    class BinaryHeader(Enum):
        SSCC_96 = "00110001"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SSCC_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid SSCC URI {epc_uri}")

        self.epc_uri = epc_uri

        self._company_pref, self._serial = self.epc_uri.split(":")[-1].split(".")

        if len(f"{self._company_pref}{self._serial}") != 17 or not (
            6 <= len(self._company_pref) <= 12
        ):
            raise ConvertException(
                message=f"Invalid SSCC URI {epc_uri} | wrong number of digits"
            )

        check_digit = calculate_checksum(
            f"{self._serial[0]}{self._company_pref}{self._serial[1:]}"
        )

        self._sscc = (
            f"{self._serial[0]}{self._company_pref}{self._serial[1:]}{check_digit}"
        )

    def gs1_key(self) -> str:
        return self._sscc

    def gs1_element_string(self) -> str:
        return f"(00){self._sscc}"

    def tag_uri(
        self,
        filter_value: SSCCFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.SSCC_96,
    ) -> str:

        return f"urn:epc:tag:{binary_coding_scheme.value}:{filter_value.value}.{self._company_pref}.{self._serial}"

    def binary(
        self,
        filter_value: SSCCFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.SSCC_96,
    ) -> str:

        parts = [self._company_pref, self._serial]

        header = SSCC.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        sscc_binary = encode_partition_table(parts, PARTITION_TABLE_L)

        return header + filter_binary + sscc_binary + "0" * 24

    @classmethod
    def from_binary(cls, binary_string: str) -> SSCC:
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        sscc_binary = truncated_binary[11:72]

        filter_string = binary_to_int(filter_binary)
        sscc_string = decode_partition_table(sscc_binary, PARTITION_TABLE_P)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{sscc_string}"
        )


def tag_to_value_sscc96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
