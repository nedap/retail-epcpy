from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    encode_partition_table,
    parse_header_and_truncate_binary,
    str_to_binary,
)
from epcpy.utils.regex import GSRNP_GS1_ELEMENT_STRING, GSRNP_URI

GSRNP_URI_REGEX = re.compile(GSRNP_URI)


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


class GSRNPFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GSRNP(TagEncodable, GS1Keyed):
    """GSRNP EPC scheme implementation.

    GSRNP pure identities are of the form:
        urn:epc:id:gsrnp:<CompanyPrefix>.<ServiceReference>

    Example:
        urn:epc:id:gsrnp:0614141.1234567890

    This class can be created using EPC pure identities via its constructor, or using:
        - GSRNP.from_gs1_element_string
        - GSRNP.from_binary
        - GSRNP.from_hex
        - GSRNP.from_base64
        - GSRNP.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        GSRNP_96 = "gsrnp-96"

    class BinaryHeader(Enum):
        GSRNP_96 = "00101110"

    gs1_element_string_regex = re.compile(GSRNP_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not GSRNP_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GSRNP URI {epc_uri}")

        self._company_pref, self._service_ref = epc_uri.split(":")[4].split(".")

        if len(f"{self._company_pref}{self._service_ref}") != 17 or not (
            6 <= len(self._company_pref) <= 12
        ):
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | wrong number of digits"
            )

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._service_ref}")

        self._gsrnp = f"{self._company_pref}{self._service_ref}{check_digit}"

    def gs1_key(self) -> str:
        """GS1 key belonging to this GSRNP instance

        Returns:
            str: GS1 key
        """
        return self._gsrnp

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(8017){self._gsrnp}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GSRNP:
        """Create a GSRNP instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: GSRNP GS1 element string invalid

        Returns:
            GSRNP: GSRNP scheme
        """
        if not GSRNP.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid GSRNP GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[6:]

        return cls(
            f"urn:epc:id:gsrnp:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}"
        )

    def tag_uri(
        self,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.GSRNP_96,
        filter_value: GSRNPFilterValue = GSRNPFilterValue.ALL_OTHERS,
    ) -> str:
        """Return the tag URI belonging to this GSRNP with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GSRNPFilterValue): Filter value

        Returns:
            str: Tag URI
        """
        filter_val = filter_value.value

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_val}.{self._company_pref}.{self._service_ref}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.GSRNP_96,
        filter_value: GSRNPFilterValue = GSRNPFilterValue.ALL_OTHERS,
    ) -> str:
        """Return the binary representation belonging to this GSRNP with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GSRNPFilterValue): Filter value

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._service_ref]

        header = GSRNP.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gsrnp_binary = encode_partition_table(parts, PARTITION_TABLE_L)

        return header + filter_binary + gsrnp_binary + "0" * 24

    @classmethod
    def from_binary(cls, binary_string: str) -> GSRNP:
        """Create an GSRNP instance from a binary string

        Args:
            binary_string (str): binary representation of an GSRNP

        Returns:
            GSRNP: GSRNP instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gsrnp_binary = truncated_binary[11:72]

        filter_string = binary_to_int(filter_binary)
        gsrnp_string = decode_partition_table(gsrnp_binary, PARTITION_TABLE_P)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gsrnp_string}"
        )
