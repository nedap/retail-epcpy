from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    decode_partition_table,
    encode_partition_table,
    parse_header_and_truncate_binary,
    replace_uri_escapes,
    revert_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from epcpy.utils.regex import GIAI_GS1_ELEMENT_STRING, GIAI_URI

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


class GIAI(TagEncodable, GS1Keyed):
    """GIAI EPC scheme implementation.

    GIAI pure identities are of the form:
        urn:epc:id:giai:<CompanyPrefix>.<IndividulAssetReference>

    Example:
        urn:epc:id:giai:0614141.12345400

    This class can be created using EPC pure identities via its constructor, or using:
        - GIAI.from_gs1_element_string
        - GIAI.from_binary
        - GIAI.from_hex
        - GIAI.from_base64
        - GIAI.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        GIAI_96 = "giai-96"
        GIAI_202 = "giai-202"

    class BinaryHeader(Enum):
        GIAI_96 = "00110100"
        GIAI_202 = "00111000"

    gs1_element_string_regex = re.compile(GIAI_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

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
        """GS1 key belonging to this GIAI instance

        Returns:
            str: GS1 key
        """
        return self._giai

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(8004){self._giai}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GIAI:
        """Create a GIAI instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: GIAI GS1 element string invalid

        Returns:
            GIAI: GIAI scheme
        """
        if not GIAI.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid GIAI GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[6 : 6 + company_prefix_length]
        chars = gs1_element_string[6 + company_prefix_length :]
        chars = revert_uri_escapes(chars)

        return cls(f"urn:epc:id:giai:{digits}.{chars}")

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: GIAIFilterValue
    ) -> str:
        """Return the tag URI belonging to this GIAI with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GIAIFilterValue): Filter value

        Raises:
            ConvertException: Asset reference value does not match requirements of provided coding scheme

        Returns:
            str: Tag URI
        """
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
        """Return the binary representation belonging to this GIAI with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GIAIFilterValue): Filter value

        Returns:
            str: binary representation
        """
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
        """Create an GIAI instance from a binary string

        Args:
            binary_string (str): binary representation of an GIAI

        Returns:
            GIAI: GIAI instance
        """
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
