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
from epcpy.utils.regex import GSRN_URI

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


class GSRNFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GSRN(EPCScheme, TagEncodable, GS1Keyed):
    class BinaryCodingScheme(Enum):
        GSRN_96 = "gsrn-96"

    class BinaryHeader(Enum):
        GSRN_96 = "00101101"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GSRN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GSRN URI {epc_uri}")

        self._company_pref, self._service_ref = epc_uri.split(":")[4].split(".")

        if len(f"{self._company_pref}{self._service_ref}") != 17 or not (
            6 <= len(self._company_pref) <= 12
        ):
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | wrong number of digits"
            )

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._service_ref}")

        self._gsrn = f"{self._company_pref}{self._service_ref}{check_digit}"

    def gs1_key(self) -> str:
        return self._gsrn

    def gs1_element_string(self) -> str:
        return f"(8018){self._gsrn}"

    def tag_uri(
        self,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.GSRN_96,
        filter_value: GSRNFilterValue = GSRNFilterValue.ALL_OTHERS,
    ) -> str:

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_value.value}.{self._company_pref}.{self._service_ref}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.GSRN_96,
        filter_value: GSRNFilterValue = GSRNFilterValue.ALL_OTHERS,
    ) -> str:

        parts = [self._company_pref, self._service_ref]

        header = GSRN.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gsrn_binary = encode_partition_table(parts, PARTITION_TABLE_L)

        return header + filter_binary + gsrn_binary + "0" * 24

    @classmethod
    def from_binary(cls, binary_string: str) -> GSRN:

        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gsrn_binary = truncated_binary[11:72]

        filter_string = binary_to_int(filter_binary)
        gsrn_string = decode_partition_table(gsrn_binary, PARTITION_TABLE_P)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gsrn_string}"
        )
