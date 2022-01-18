from typing import Any

from common import BinaryCodingSchemes, hex_to_base64


class EPC_SCHEME:
    def __init__(self) -> None:
        self._base64 = None
        self._binary = None
        self._hex = None
        self._tag_uri = None

    def hex(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        if self._hex:
            return self._hex

        if binary_coding_scheme:
            binary = self.binary(binary_coding_scheme, filter_value)
        else:
            binary = self.binary(filter_value)

        padding = (16 - (len(binary) % 16)) % 16
        padded_binary = f"{binary:<0{len(binary) + padding}}"

        self._hex = f"{int(padded_binary, 2):X}"

        return self._hex

    def base64(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        if self._base64:
            return self._base64

        hex_string = self.hex(binary_coding_scheme, filter_value)

        self._base64 = hex_to_base64(hex_string)

        return self._base64

    def calculate_checksum(self, digits: str) -> int:
        digits = [int(d) for d in digits]
        odd, even = digits[1::2], digits[0::2]

        if len(digits) % 2 == 0:
            val1 = sum(even)
            val2 = sum(odd)
        else:
            val1 = sum(odd)
            val2 = sum(even)

        checksum = (10 - ((3 * (val1) + (val2)) % 10)) % 10

        return checksum
