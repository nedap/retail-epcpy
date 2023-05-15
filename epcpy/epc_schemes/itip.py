from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import GS1Element, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_fixed_width_integer,
    decode_partition_table,
    decode_string,
    encode_fixed_width_integer,
    encode_partition_table,
    encode_string,
    parse_header_and_truncate_binary,
    replace_uri_escapes,
    revert_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from epcpy.utils.regex import ITIP_GS1_ELEMENT_STRING, ITIP_URI

ITIP_URI_REGEX = re.compile(ITIP_URI)

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


class ITIPFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class ITIP(GS1Element, TagEncodable):
    """ITIP EPC scheme implementation.

    ITIP pure identities are of the form:
        urn:epc:id:itip:<CompanyPrefix>.<ItemRefAndIndicator>.<Piece>.<Total>.<SerialNumber>

    Example:
        urn:epc:id:itip:4012345.012345.01.02.987

    This class can be created using EPC pure identities via its constructor, or using:
        - ITIP.from_gs1_element_string
        - ITIP.from_binary
        - ITIP.from_hex
        - ITIP.from_base64
        - ITIP.from_tag_uri

    Attributes:
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        ITIP_110 = "itip-110"
        ITIP_212 = "itip-212"

    class BinaryHeader(Enum):
        ITIP_110 = "01000000"
        ITIP_212 = "01000001"

    gs1_element_string_regex = re.compile(ITIP_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not ITIP_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid ITIP URI {epc_uri}")

        (
            self._company_pref,
            self._item_ref,
            self._piece,
            self._total,
            *serial,
        ) = ":".join(epc_uri.split(":")[4:]).split(".")

        self._serial = ".".join(serial)
        verify_gs3a3_component(self._serial)

        if (
            len(f"{self._company_pref}{self._item_ref}{self._piece}{self._total}") != 17
            or not (1 <= len(replace_uri_escapes(self._serial)) <= 20)
            or not (6 <= len(self._company_pref) <= 12)
        ):
            raise ConvertException(message=f"Invalid ITIP URI {epc_uri}")

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        indicator = self._item_ref[0]

        check_digit = calculate_checksum(
            f"{indicator}{self._company_pref}{self._item_ref[1:]}"
        )
        return f"(8006){indicator}{self._company_pref}{self._item_ref[1:]}{check_digit}{self._piece}{self._total}(21){replace_uri_escapes(self._serial)}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> ITIP:
        """Create a ITIP instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: ITIP GS1 element string invalid

        Returns:
            ITIP: ITIP scheme
        """
        if not ITIP.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid ITIP GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[6:24]
        chars = gs1_element_string[28:]
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:itip:{digits[1:1+company_prefix_length]}.{digits[0]}{digits[1+company_prefix_length:-5]}.{digits[-4:-2]}.{digits[-2:]}.{chars}"
        )

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: ITIPFilterValue
    ) -> str:
        """Return the tag URI belonging to this ITIP with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (ITIPFilterValue): Filter value

        Raises:
            ConvertException: Serial does not match requirements of provided coding scheme

        Returns:
            str: Tag URI
        """
        filter_val = filter_value.value

        if (
            binary_coding_scheme == ITIP.BinaryCodingScheme.ITIP_212
            and len(replace_uri_escapes(self._serial)) > 20
        ) or (
            binary_coding_scheme == ITIP.BinaryCodingScheme.ITIP_110
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 38)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_val}.{self._company_pref}.{self._item_ref}.{self._piece}.{self._total}.{self._serial}"

    def binary(
        self,
        filter_value: ITIPFilterValue,
        binary_coding_scheme: BinaryCodingScheme,
    ) -> str:
        """Return the binary representation belonging to this ITIP with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (ITIPFilterValue): Filter value

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._item_ref]

        header = ITIP.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gtin_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        piece_binary = encode_fixed_width_integer(self._piece, 7)
        total_binary = encode_fixed_width_integer(self._total, 7)
        serial_binary = (
            str_to_binary(self._serial, 38)
            if binary_coding_scheme == ITIP.BinaryCodingScheme.ITIP_110
            else encode_string(self._serial, 140)
        )

        return (
            header
            + filter_binary
            + gtin_binary
            + piece_binary
            + total_binary
            + serial_binary
        )

    @classmethod
    def from_binary(cls, binary_string: str) -> ITIP:
        """Create an ITIP instance from a binary string

        Args:
            binary_string (str): binary representation of an ITIP

        Returns:
            ITIP: ITIP instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gtin_binary = truncated_binary[11:58]
        piece_binary = truncated_binary[58:65]
        total_binary = truncated_binary[65:72]
        serial_binary = truncated_binary[72:]

        filter_string = binary_to_int(filter_binary)
        gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)
        piece_string = decode_fixed_width_integer(piece_binary)
        total_string = decode_fixed_width_integer(total_binary)
        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == ITIP.BinaryCodingScheme.ITIP_110
            else decode_string(serial_binary)
        )

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gtin_string}.{piece_string}.{total_string}.{serial_string}"
        )
