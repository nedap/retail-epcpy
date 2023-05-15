from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    decode_cage_code,
    encode_cage_code,
    parse_header_and_truncate_binary,
    str_to_binary,
)
from epcpy.utils.regex import USDOD_URI

USDOD_URI_REGEX = re.compile(USDOD_URI)


class USDODFilterValue(Enum):
    PALLET = "0"
    CASE = "1"
    UNIT_PACK = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"
    RESERVED_8 = "8"
    RESERVED_9 = "9"
    RESERVED_10 = "10"
    RESERVED_11 = "11"
    RESERVED_12 = "12"
    RESERVED_13 = "13"
    RESERVED_14 = "14"
    RESERVED_15 = "15"


class USDOD(TagEncodable):
    """USDOD EPC scheme implementation.

    USDOD pure identities are of the form:
        urn:epc:id:usdod:<CAGEOrDODAAC>.<SerialNumber>

    Example:
        urn:epc:id:usdod:2S194.12345678901

    This class can be created using EPC pure identities via its constructor, or using:
        - USDOD.from_binary
        - USDOD.from_hex
        - USDOD.from_base64
        - USDOD.from_tag_uri

    Attributes:
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        USDOD_96 = "usdod-96"

    class BinaryHeader(Enum):
        USDOD_96 = "00101111"

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not USDOD_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid USDOD URI {epc_uri}")

        self._cage_dodaac, self._serial = epc_uri.split(":")[4].split(".")

        if int(self._serial) >= pow(2, 36) or (
            len(self._serial) > 1 and self._serial[0] == "0"
        ):
            raise ConvertException(message=f"Serial out of range: (max: {pow(2, 36)})")

        self.epc_uri = epc_uri

    def tag_uri(
        self,
        filter_value: USDODFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.USDOD_96,
    ) -> str:
        """Return the tag URI belonging to this USDOD with the provided binary coding scheme and filter value.

        Args:
            filter_value (USDODFilterValue): Filter value
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
                Defaults to BinaryCodingScheme.USDOD_96

        Returns:
            str: Tag URI
        """
        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_value.value}.{self._cage_dodaac}.{self._serial}"

    def binary(
        self,
        filter_value: USDODFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.USDOD_96,
    ) -> str:
        """Return the binary representation belonging to this USDOD with the provided binary coding scheme and filter value.

        Args:
            filter_value (USDODFilterValue): Filter value
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
                Defaults to BinaryCodingScheme.USDOD_96

        Returns:
            str: binary representation
        """
        header = USDOD.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 4)
        cage_code_binary = encode_cage_code(f"{self._cage_dodaac:>6}")
        serial_binary = str_to_binary(self._serial, 36)

        return header + filter_binary + cage_code_binary + serial_binary

    @classmethod
    def from_binary(cls, binary_string: str) -> USDOD:
        """Create an USDOD instance from a binary string

        Args:
            binary_string (str): binary representation of an USDOD

        Returns:
            USDOD: USDOD instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:12]
        cage_code_binary = truncated_binary[12:60]
        serial_binary = truncated_binary[60:]

        filter_string = binary_to_int(filter_binary)
        cage_code_string = decode_cage_code(cage_code_binary)
        serial_string = binary_to_int(serial_binary)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{cage_code_string}.{serial_string}"
        )
