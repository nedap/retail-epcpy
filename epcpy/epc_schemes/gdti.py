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
from epcpy.utils.regex import GDTI_GS1_ELEMENT_STRING, GDTI_URI

GDTI_URI_REGEX = re.compile(GDTI_URI)

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


class GDTIFilterValue(Enum):
    ALL_OTHERS = "0"
    TRAVEL_DOCUMENT = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GDTI(TagEncodable, GS1Keyed):
    """GDTI EPC scheme implementation.

    GDTI pure identities are of the form:
        urn:epc:id:gdti:<CompanyPrefix>.<DocumentType>.<SerialNumber>

    Example:
        urn:epc:id:gdti:0614141.12345.400

    This class can be created using EPC pure identities via its constructor, or using:
        - GDTI.from_gs1_element_string
        - GDTI.from_binary
        - GDTI.from_hex
        - GDTI.from_base64
        - GDTI.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        GDTI_96 = "gdti-96"
        GDTI_174 = "gdti-174"

    class BinaryHeader(Enum):
        GDTI_96 = "00101100"
        GDTI_174 = "00111110"

    gs1_element_string_regex = re.compile(GDTI_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not GDTI_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GDTI URI {epc_uri}")

        self._serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(self._serial)

        self._company_pref, self._doc_type = epc_uri.split(":")[4].split(".")[:2]

        if (
            len(f"{self._company_pref}{self._doc_type}") != 12
            or len(self._serial) > 17
            or not (6 <= len(self._company_pref) <= 12)
        ):
            raise ConvertException(
                message=f"Invalid GDTI URI {epc_uri} | Company prefix + document type must be 12 digits"
            )

        self.epc_uri = epc_uri
        check_digit = calculate_checksum(f"{self._company_pref}{self._doc_type}")

        self._gdti = f"{self._company_pref}{self._doc_type}{check_digit}{replace_uri_escapes(self._serial)}"

    def gs1_key(self) -> str:
        """GS1 key belonging to this GDTI instance

        Returns:
            str: GS1 key
        """
        return self._gdti

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(253){self._gdti}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GDTI:
        """Create a GDTI instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: GDTI GS1 element string invalid

        Returns:
            GDTI: GDTI scheme
        """
        if not GDTI.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid GDTI GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[5:18]
        chars = gs1_element_string[18:]
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:gdti:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}.{chars}"
        )

    def tag_uri(
        self,
        binary_coding_scheme: GDTI.BinaryCodingScheme,
        filter_value: GDTIFilterValue,
    ) -> str:
        """Return the tag URI belonging to this GDTI with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GDTIFilterValue): Filter value

        Raises:
            ConvertException: Serial does not match requirements of provided coding scheme

        Returns:
            str: Tag URI
        """
        scheme = binary_coding_scheme.value
        filter_val = filter_value.value

        if (
            scheme == GDTI.BinaryCodingScheme.GDTI_174.value
            and len(replace_uri_escapes(self._serial)) > 17
        ) or (
            scheme == GDTI.BinaryCodingScheme.GDTI_96.value
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 41)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        return f"{self.TAG_URI_PREFIX}{scheme}:{filter_val}.{self._company_pref}.{self._doc_type}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: GDTIFilterValue,
    ) -> str:
        """Return the binary representation belonging to this GDTI with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GDTIFilterValue): Filter value

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._doc_type]

        header = GDTI.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gdti_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(self._serial, 41)
            if binary_coding_scheme == GDTI.BinaryCodingScheme.GDTI_96
            else encode_string(self._serial, 119)
        )

        _binary = header + filter_binary + gdti_binary + serial_binary
        return _binary

    @classmethod
    def from_binary(cls, binary_string: str) -> GDTI:
        """Create an GDTI instance from a binary string

        Args:
            binary_string (str): binary representation of an GDTI

        Returns:
            GDTI: GDTI instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gdti_binary = truncated_binary[11:55]
        serial_binary = truncated_binary[55:]

        filter_string = binary_to_int(filter_binary)
        gdti_string = decode_partition_table(gdti_binary, PARTITION_TABLE_P)

        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == GDTI.BinaryCodingScheme.GDTI_96
            else decode_string(serial_binary)
        )
        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gdti_string}.{serial_string}"
        )
