from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_pure_identities.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    decode_partition_table,
    encode_partition_table,
    parse_header_and_truncate_binary,
    replace_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from epcpy.utils.regex import GIAI_URI

GIAI_URI_REGEX = re.compile(GIAI_URI)

PARTITION_TABLE_P_96 = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 42,
        "K": 13,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 45,
        "K": 14,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 48,
        "K": 15,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 52,
        "K": 16,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 55,
        "K": 17,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 58,
        "K": 18,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 62,
        "K": 19,
    },
}

PARTITION_TABLE_L_96 = {
    12: PARTITION_TABLE_P_96[0],
    11: PARTITION_TABLE_P_96[1],
    10: PARTITION_TABLE_P_96[2],
    9: PARTITION_TABLE_P_96[3],
    8: PARTITION_TABLE_P_96[4],
    7: PARTITION_TABLE_P_96[5],
    6: PARTITION_TABLE_P_96[6],
}

PARTITION_TABLE_P_202 = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 148,
        "K": 18,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 151,
        "K": 19,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 154,
        "K": 20,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 158,
        "K": 21,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 161,
        "K": 22,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 164,
        "K": 23,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 168,
        "K": 24,
    },
}

PARTITION_TABLE_L_202 = {
    12: PARTITION_TABLE_P_202[0],
    11: PARTITION_TABLE_P_202[1],
    10: PARTITION_TABLE_P_202[2],
    9: PARTITION_TABLE_P_202[3],
    8: PARTITION_TABLE_P_202[4],
    7: PARTITION_TABLE_P_202[5],
    6: PARTITION_TABLE_P_202[6],
}


class GIAIFilterValue(Enum):
    ALL_OTHERS = "0"
    RAIL_VEHICLE = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GIAI(EPCScheme, TagEncodable, GS1Keyed):
    class BinaryCodingScheme(Enum):
        GIAI_96 = "giai-96"
        GIAI_202 = "giai-202"

    class BinaryHeader(Enum):
        GIAI_96 = "00110100"
        GIAI_202 = "00111000"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GIAI_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GIAI URI {epc_uri}")

        company_prefix, *asset_reference = epc_uri.split(":")[4].split(".")
        asset_reference = ".".join(asset_reference)

        if (
            not (6 <= len(company_prefix) <= 12)
            or len(f"{company_prefix}{asset_reference}") > 30
        ):
            raise ConvertException(
                message=f"Invalid company prefix length {len(company_prefix)}"
            )

        verify_gs3a3_component(asset_reference)

        self.epc_uri = epc_uri

        self._company_pref = company_prefix
        self._asset_ref = asset_reference
        self._giai = f"{company_prefix}{replace_uri_escapes(asset_reference)}"

    def gs1_key(self) -> str:
        return self._giai

    def gs1_element_string(self) -> str:
        return f"(8004){self._giai}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: GIAIFilterValue
    ) -> str:
        filter_val = filter_value.value

        if (
            binary_coding_scheme == GIAI.BinaryCodingScheme.GIAI_202
            and len(replace_uri_escapes(self._asset_ref))
            > PARTITION_TABLE_L_202[len(self._company_pref)]["K"]
        ) or (
            binary_coding_scheme == GIAI.BinaryCodingScheme.GIAI_96
            and (
                not self._asset_ref.isnumeric()
                or len(self._asset_ref)
                > PARTITION_TABLE_L_96[len(self._company_pref)]["K"]
                or int(self._asset_ref)
                >= pow(2, PARTITION_TABLE_L_96[len(self._company_pref)]["N"])
                or (len(self._asset_ref) > 1 and self._asset_ref[0] == "0")
            )
        ):
            raise ConvertException(
                message=f"Invalid asset reference value {self._asset_ref}"
            )

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_val}.{self._company_pref}.{self._asset_ref}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: GIAIFilterValue,
    ) -> str:

        header = GIAI.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        parts = [self._company_pref, self._asset_ref]

        giai_binary = (
            encode_partition_table(parts, PARTITION_TABLE_L_96)
            if binary_coding_scheme == GIAI.BinaryCodingScheme.GIAI_96
            else encode_partition_table(
                parts,
                PARTITION_TABLE_L_202,
                string_partition=True,
            )
        )

        _binary = header + filter_binary + giai_binary
        return _binary

    @classmethod
    def from_binary(cls, binary_string: str) -> GIAI:
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )
        filter_binary = truncated_binary[8:11]
        giai_binary = truncated_binary[11:]

        filter_string = binary_to_int(filter_binary)

        giai_string = (
            decode_partition_table(
                giai_binary, PARTITION_TABLE_P_96, unpadded_partition=True
            )
            if binary_coding_scheme == GIAI.BinaryCodingScheme.GIAI_96
            else decode_partition_table(
                giai_binary, PARTITION_TABLE_P_202, string_partition=True
            )
        )

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{giai_string}"
        )
