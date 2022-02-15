from __future__ import annotations
import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, TagEncodable
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


class USDOD(EPCScheme, TagEncodable):
    class BinaryCodingScheme(Enum):
        USDOD_96 = "usdod-96"

    class BinaryHeader(Enum):
        USDOD_96 = "00101111"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not USDOD_URI_REGEX.match(epc_uri):
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

        return f"urn:epc:tag:{binary_coding_scheme.USDOD_96.value}:{filter_value.value}.{self._cage_dodaac}.{self._serial}"

    def binary(
        self,
        filter_value: USDODFilterValue,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.USDOD_96,
    ) -> str:

        header = USDOD.BinaryHeader[binary_coding_scheme.USDOD_96.name].value
        filter_binary = str_to_binary(filter_value.value, 4)
        cage_code_binary = encode_cage_code(f"{self._cage_dodaac:>6}")
        serial_binary = str_to_binary(self._serial, 36)

        return header + filter_binary + cage_code_binary + serial_binary

    @classmethod
    def from_binary(cls, binary_string: str) -> USDOD:
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )


def binary_to_value_usdod96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:12]
    cage_code_binary = truncated_binary[12:60]
    serial_binary = truncated_binary[60:]

    filter_string = binary_to_int(filter_binary)
    cage_code_string = decode_cage_code(cage_code_binary)
    serial_string = binary_to_int(serial_binary)

    return f"{filter_string}.{cage_code_string}.{serial_string}"


def tag_to_value_usdod96(epc_tag_uri: str) -> str:
    return ".".join(epc_tag_uri.split(":")[4].split(".")[1:])
