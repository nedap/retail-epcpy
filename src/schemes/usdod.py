import re
from enum import Enum

from base_scheme import EPCScheme
from common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    str_to_binary,
)
from regex import USDOD_URI

USDOD_URI_REGEX = re.compile(USDOD_URI)


class USDODFilterValues(Enum):
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


def decode_cage_code(binary: str) -> str:
    return "".join(
        [chr(int(g, 2)) if g != "" else "" for g in re.split("([0-1]{8})", binary)]
    ).replace(" ", "")


def encode_cage_code(chars: str) -> str:
    return "".join([f"{ord(char):0>8b}" for char in chars])


class USDOD(EPCScheme):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not USDOD_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        self.cage_dodaac, self.serial = epc_uri.split(":")[4].split(".")

        if int(self.serial) >= pow(2, 36) or (
            len(self.serial) > 1 and self.serial[0] == "0"
        ):
            raise ConvertException(message=f"Serial out of range: (max: {pow(2, 36)})")

        self.epc_uri = epc_uri

    def tag_uri(self, filter_value: USDODFilterValues) -> str:
        if self._tag_uri:
            return self._tag_uri

        if filter_value is None:
            raise ConvertException(
                message="Either tag_uri should be set or a filter value should be provided"
            )

        scheme = BinaryCodingSchemes.USDOD_96.value
        filter_val = filter_value.value
        value = self.epc_uri.split(":")[4]

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{value}"

        return self._tag_uri

    def binary(self, filter_value: USDODFilterValues = None) -> str:
        if self._binary:
            return self._binary

        self.tag_uri(filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_val = self._tag_uri.split(":")[4].split(".")[0]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_val, 4)
        cage_code_binary = encode_cage_code(f"{self.cage_dodaac:>6}")
        serial_binary = str_to_binary(self.serial, 36)

        self._binary = header + filter_binary + cage_code_binary + serial_binary
        return self._binary


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
