from __future__ import annotations

import re
from enum import Enum, IntEnum

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
from epcpy.utils.regex import SGTIN_GS1_ELEMENT_STRING, SGTIN_URI

SGTIN_REGEX = re.compile(SGTIN_URI)

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


class SGTINFilterValue(Enum):
    ALL_OTHERS = "0"
    POS_ITEM = "1"
    FULL_CASE = "2"
    RESERVED_3 = "3"
    INNER_PACK = "4"
    RESERVED_5 = "5"
    UNIT_LOAD = "6"
    COMPONENT = "7"


class GTIN_TYPE(IntEnum):
    GTIN8 = (8,)
    GTIN12 = (12,)
    GTIN13 = (13,)
    GTIN14 = 14


class SGTIN(TagEncodable, GS1Keyed):
    """SGTIN EPC scheme implementation.

    SGTIN pure identities are of the form:
        urn:epc:id:sgtin:<CompanyPrefix>.<ItemRefAndIndicator>.<SerialNumber>

    Example:
        urn:epc:id:sgtin:0614141.112345.400

    This class can be created using EPC pure identities via its constructor, or using:
        - SGTIN.from_gtin_plus_serial
        - SGTIN.from_gs1_element_string
        - SGTIN.from_binary
        - SGTIN.from_hex
        - SGTIN.from_base64
        - SGTIN.from_tag_uri

    Attributes:
        gs1_key (str): GS1 key
        gtin (str): GTIN
        gs1_element_string (str): GS1 element string
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        SGTIN_96 = "sgtin-96"
        SGTIN_198 = "sgtin-198"

    class BinaryHeader(Enum):
        SGTIN_96 = "00110000"
        SGTIN_198 = "00110110"

    gs1_element_string_regex = re.compile(SGTIN_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not SGTIN_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid SGTIN URI {epc_uri}")

        self.epc_uri = epc_uri

        value = self.epc_uri.split(":")[4]
        self._company_pref = value.split(".")[0]
        self._item_ref = value.split(".")[1]
        self._serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])

        if len(f"{self._company_pref}{self._item_ref}") != 13 or not (
            6 <= len(self._company_pref) <= 12
        ):
            raise ConvertException(
                message=f"Invalid SGTIN URI {epc_uri} | Company prefix + item reference must be 13 digits"
            )

        verify_gs3a3_component(self._serial)

        if not (1 <= len(replace_uri_escapes(self._serial)) <= 20):
            raise ConvertException(
                message=f"Invalid number of characters in serial: {len(replace_uri_escapes(self._serial))}"
            )

        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )

        self._gtin = f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}".zfill(
            14
        )

    @classmethod
    def from_gtin_plus_serial(
        cls, gtin: str, serial: str, company_prefix_length: int
    ) -> SGTIN:
        """Create an SGTIN class from a gtin, serial and company prefix length

        Args:
            gtin (str): GTIN
            serial (str): Serial value
            company_prefix_length (int): Length of company prefix

        Returns:
            SGTIN: Instance of SGTIN class based on the provided data
        """
        gtin = gtin.zfill(14)
        return cls(
            f"urn:epc:id:sgtin:{gtin[1:1 + company_prefix_length]}.{gtin[0]}{gtin[1 + company_prefix_length:-1]}.{str(serial)}"
        )

    def gs1_key(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        """GS1 key belonging to this SGTIN instance

        Args:
            gtin_type (GTIN_TYPE, optional): What GTIN length to return.
                Defaults to GTIN_TYPE.GTIN14.

        Returns:
            str: GS1 key
        """
        return self.gtin(gtin_type=gtin_type)

    def gtin(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        """GTIN belonging to this SGTIN instance

        Args:
            gtin_type (GTIN_TYPE, optional): What GTIN length to return.
                Defaults to GTIN_TYPE.GTIN14.

        Raises:
            ConvertException: GTIN does not match given

        Returns:
            str: GTIN
        """
        if gtin_type != GTIN_TYPE.GTIN14:
            if not self._gtin.startswith((14 - gtin_type) * "0"):
                raise ConvertException(message=f"Invalid GTIN{gtin_type}")

        return self._gtin[14 - gtin_type : 14]

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        gtin = self._gtin
        serial = replace_uri_escapes(self._serial)

        return f"(01){gtin}(21){serial}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> SGTIN:
        """Create a SGTIN instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: SGTIN GS1 element string invalid

        Returns:
            SGTIN: SGTIN scheme
        """
        if not SGTIN.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid SGTIN GS1 element string {gs1_element_string}"
            )

        _, digits, chars = re.split(f"\(.{{2}}\)", gs1_element_string)
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:sgtin:{digits[1:company_prefix_length+1]}.{digits[0]}{digits[1+company_prefix_length:-1]}.{chars}"
        )

    def tag_uri(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: SGTINFilterValue,
    ) -> str:
        """Return the tag URI belonging to this SGTIN with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (SGTINFilterValue): Filter value

        Raises:
            ConvertException: Serial does not match requirements of provided coding scheme

        Returns:
            str: Tag URI
        """
        if binary_coding_scheme == SGTIN.BinaryCodingScheme.SGTIN_96 and (
            not self._serial.isnumeric()
            or int(self._serial) >= pow(2, 38)
            or (len(self._serial) > 1 and self._serial[0] == "0")
        ):
            raise ConvertException(
                message=f"Invalid serial value {self._serial} for SGTIN_96 coding scheme"
            )

        scheme = binary_coding_scheme.value
        filter_val = filter_value.value

        return f"{self.TAG_URI_PREFIX}{scheme}:{filter_val}.{self._company_pref}.{self._item_ref}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: SGTINFilterValue,
    ) -> str:
        """Return the binary representation belonging to this SGTIN with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (SGTINFilterValue): Filter value

        Returns:
            str: binary representation
        """
        parts = [self._company_pref, self._item_ref]

        header = SGTIN.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gtin_binary = encode_partition_table(parts, PARTITION_TABLE_L)

        serial_binary = (
            str_to_binary(self._serial, 38)
            if binary_coding_scheme == SGTIN.BinaryCodingScheme.SGTIN_96
            else encode_string(self._serial, 140)
        )

        return header + filter_binary + gtin_binary + serial_binary

    @classmethod
    def from_binary(cls, binary_string: str) -> SGTIN:
        """Create an SGTIN instance from a binary string

        Args:
            binary_string (str): binary representation of an SGTIN

        Returns:
            SGTIN: SGTIN instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gtin_binary = truncated_binary[11:58]
        serial_binary = truncated_binary[58:]

        filter_string = binary_to_int(filter_binary)
        gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)

        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == SGTIN.BinaryCodingScheme.SGTIN_96
            else decode_string(serial_binary)
        )

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gtin_string}.{serial_string}"
        )
