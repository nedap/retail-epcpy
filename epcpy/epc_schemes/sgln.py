from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    decode_string,
    encode_partition_table,
    encode_string,
    parse_header_and_truncate_binary,
    replace_uri_escapes,
    revert_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from epcpy.utils.regex import SGLN_GS1_ELEMENT_STRING, SGLN_URI

SGLN_URI_REGEX = re.compile(SGLN_URI)

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


class SGLNFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class SGLN(TagEncodable, GS1Keyed):
    """SGLN EPC scheme implementation.

    SGLN pure identities are of the form:
        urn:epc:id:sgln:<CompanyPrefix>.<LocationReference>.<Extension>

    Example:
        urn:epc:id:sgln:0614141.12345.400

    This class can be created using EPC pure identities via its constructor, or using:
        - SGLN.from_gs1_element_string
        - SGLN.from_binary
        - SGLN.from_hex
        - SGLN.from_base64
        - SGLN.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        SGLN_96 = "sgln-96"
        SGLN_195 = "sgln-195"

    class BinaryHeader(Enum):
        SGLN_96 = "00110010"
        SGLN_195 = "00111001"

    gs1_element_string_regex = re.compile(SGLN_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not SGLN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid SGLN URI {epc_uri}")

        self._company_pref, self._location_ref = epc_uri.split(":")[4].split(".")[:2]
        self._serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])

        if (
            len(f"{self._company_pref}{self._location_ref}") != 12
            or not (6 <= len(self._company_pref) <= 12)
            or len(replace_uri_escapes(self._serial)) > 20
        ):
            raise ConvertException(
                message=f"Invalid SGLN URI {epc_uri} | Company prefix + location reference must be 12 digits"
            )

        verify_gs3a3_component(self._serial)

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._location_ref}")
        self._gln = f"{self._company_pref}{self._location_ref}{check_digit}"

    def gs1_key(self) -> str:
        """Returns the GS1 key

        Returns:
            str: GS1 key
        """
        return self._gln

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        extension = replace_uri_escapes(self._serial)
        return f"(414){self._gln}(254){extension}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> SGLN:
        """Create a SGLN instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: SGLN GS1 element string invalid

        Returns:
            SGLN: SGLN scheme
        """
        if not SGLN.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid SGLN GS1 element string {gs1_element_string}"
            )

        _, digits, chars = re.split(f"\(.{{3}}\)", gs1_element_string)
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:sgln:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}.{chars}"
        )

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: SGLNFilterValue
    ) -> str:
        """Return the tag URI belonging to this SGLN with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (SGLNFilterValue): Filter value

        Raises:
            ConvertException: Serial does not match requirements of provided coding scheme

        Returns:
            str: Tag URI
        """
        if (
            binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_195
            and len(replace_uri_escapes(self._serial)) > 20
        ) or (
            binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_96
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 41)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_value.value}.{self._company_pref}.{self._location_ref}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: SGLNFilterValue,
    ) -> str:
        """Return the binary representation belonging to this SGLN with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (SGLNFilterValue): Filter value

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._location_ref]

        header = SGLN.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gln_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(self._serial, 41)
            if binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_96
            else encode_string(self._serial, 140)
        )

        return header + filter_binary + gln_binary + serial_binary

    @classmethod
    def from_binary(cls, binary_string: str) -> SGLN:
        """Create an SGLN instance from a binary string

        Args:
            binary_string (str): binary representation of an SGLN

        Returns:
            SGLN: SGLN instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gln_binary = truncated_binary[11:55]
        serial_binary = truncated_binary[55:]

        filter_string = binary_to_int(filter_binary)
        gln_string = decode_partition_table(gln_binary, PARTITION_TABLE_P)
        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_96
            else decode_string(serial_binary)
        )

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gln_string}.{serial_string}"
        )
