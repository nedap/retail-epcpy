from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_numeric_string,
    decode_partition_table,
    encode_numeric_string,
    encode_partition_table,
    parse_header_and_truncate_binary,
    revert_uri_escapes,
    str_to_binary,
)
from epcpy.utils.regex import SGCN_GS1_ELEMENT_STRING, SGCN_URI

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


class SGCNFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class SGCN(TagEncodable, GS1Keyed):
    """SGCN EPC scheme implementation.

    SGCN pure identities are of the form:
        urn:epc:id:sgcn:<CompanyPrefix>.<CouponReference>.<SerialComponent>

    Example:
        urn:epc:id:sgcn:4012345.67890.04711

    This class can be created using EPC pure identities via its constructor, or using:
        - SGCN.from_gs1_element_string
        - SGCN.from_binary
        - SGCN.from_hex
        - SGCN.from_base64
        - SGCN.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        SGCN_96 = "sgcn-96"

    class BinaryHeader(Enum):
        SGCN_96 = "00111111"

    gs1_element_string_regex = re.compile(SGCN_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

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
        """Returns the GS1 key

        Returns:
            str: GS1 key
        """
        return self._gcn

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(255){self._gcn}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> SGCN:
        """Create a SGCN instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: SGCN GS1 element string invalid

        Returns:
            SGCN: SGCN scheme
        """
        if not SGCN.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid SGCN GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[5:18]
        chars = gs1_element_string[18:]
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:sgcn:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}.{chars}"
        )

    def tag_uri(
        self,
        filter_value: SGCNFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.SGCN_96,
    ) -> str:
        """Return the tag URI belonging to this SGCN with the provided binary coding scheme and filter value.

        Args:
            filter_value (SGCNFilterValue): Filter value
            binary_coding_scheme (BinaryCodingScheme, optional): Coding scheme
                Defaults to BinaryCodingScheme.SGCN_96

        Returns:
            str: Tag URI
        """
        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_value.value}.{self._company_pref}.{self._coupon_ref}.{self._serial}"

    def binary(
        self,
        filter_value: SGCNFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.SGCN_96,
    ) -> str:
        """Return the binary representation belonging to this SGCN with the provided binary coding scheme and filter value.

        Args:
            filter_value (SGCNFilterValue): Filter value
            binary_coding_scheme (BinaryCodingScheme, optional): Coding scheme
                Defaults to BinaryCodingScheme.SGCN_96

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._coupon_ref]

        header = SGCN.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        sgcn_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = encode_numeric_string(self._serial, 41)

        return header + filter_binary + sgcn_binary + serial_binary

    @classmethod
    def from_binary(cls, binary_string: str) -> SGCN:
        """Create an SGCN instance from a binary string

        Args:
            binary_string (str): binary representation of an SGCN

        Returns:
            SGCN: SGCN instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        sgcn_binary = truncated_binary[11:55]
        serial_binary = truncated_binary[55:]

        filter_string = binary_to_int(filter_binary)
        sgcn_string = decode_partition_table(sgcn_binary, PARTITION_TABLE_P)
        serial_string = decode_numeric_string(serial_binary)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{sgcn_string}.{serial_string}"
        )
