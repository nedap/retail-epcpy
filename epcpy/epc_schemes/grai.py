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
from epcpy.utils.regex import GRAI_GS1_ELEMENT_STRING, GRAI_URI

GRAI_URI_REGEX = re.compile(GRAI_URI)

PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 4,
        "K": 0,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 7,
        "K": 1,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 10,
        "K": 2,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 14,
        "K": 3,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 17,
        "K": 4,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 20,
        "K": 5,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 24,
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


class GRAIFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GRAI(TagEncodable, GS1Keyed):
    """GRAI EPC scheme implementation.

    GRAI pure identities are of the form:
        urn:epc:id:grai:<CompanyPrefix>.<AssetType>.<SerialNumber>

    Example:
        urn:epc:id:grai:0614141.12345.400

    This class can be created using EPC pure identities via its constructor, or using:
        - GRAI.from_gs1_element_string
        - GRAI.from_binary
        - GRAI.from_hex
        - GRAI.from_base64
        - GRAI.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        GRAI_96 = "grai-96"
        GRAI_170 = "grai-170"

    class BinaryHeader(Enum):
        GRAI_96 = "00110011"
        GRAI_170 = "00110111"

    gs1_element_string_regex = re.compile(GRAI_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not GRAI_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GRAI URI {epc_uri}")

        self._serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(self._serial)

        self._company_pref, self._asset_type = epc_uri.split(":")[4].split(".")[:2]

        if (
            len(f"{self._company_pref}{self._asset_type}") != 12
            or not (6 <= len(self._company_pref) <= 12)
            or len(self._serial) > 16
        ):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._asset_type}")
        self._grai = f"{self._company_pref}{self._asset_type}{check_digit}{replace_uri_escapes(self._serial)}"

    def gs1_key(self) -> str:
        """GS1 key belonging to this GRAI instance

        Returns:
            str: GS1 key
        """
        return self._grai

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(8003)0{self._grai}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GRAI:
        """Create a GRAI instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: GRAI GS1 element string invalid

        Returns:
            GRAI: GRAI scheme
        """
        if not GRAI.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid GRAI GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[7:20]
        chars = gs1_element_string[20:]
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:grai:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}.{chars}"
        )

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: GRAIFilterValue
    ) -> str:
        """Return the tag URI belonging to this GRAI with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GRAIFilterValue): Filter value

        Raises:
            ConvertException: Serial does not match requirements of provided coding scheme

        Returns:
            str: Tag URI
        """
        filter_val = filter_value.value

        if (
            binary_coding_scheme == GRAI.BinaryCodingScheme.GRAI_170
            and len(replace_uri_escapes(self._serial)) > 20
        ) or (
            binary_coding_scheme == GRAI.BinaryCodingScheme.GRAI_96
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 38)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_val}.{self._company_pref}.{self._asset_type}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: GRAIFilterValue,
    ) -> str:
        """Return the binary representation belonging to this GRAI with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GRAIFilterValue): Filter value

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._asset_type]

        header = GRAI.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        grai_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(self._serial, 38)
            if binary_coding_scheme == GRAI.BinaryCodingScheme.GRAI_96
            else encode_string(self._serial, 112)
        )

        _binary = header + filter_binary + grai_binary + serial_binary
        return _binary

    @classmethod
    def from_binary(cls, binary_string: str) -> GRAI:
        """Create an GRAI instance from a binary string

        Args:
            binary_string (str): binary representation of an GRAI

        Returns:
            GRAI: GRAI instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        grai_binary = truncated_binary[11:58]
        serial_binary = truncated_binary[58:]

        filter_string = binary_to_int(filter_binary)
        grai_string = decode_partition_table(grai_binary, PARTITION_TABLE_P)

        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == GRAI.BinaryCodingScheme.GRAI_96
            else decode_string(serial_binary)
        )

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{grai_string}.{serial_string}"
        )
