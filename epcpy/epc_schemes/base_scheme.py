from __future__ import annotations
from enum import Enum
from epcpy.utils.common import ConvertException, hex_to_base64, hex_to_binary


class EPCScheme:
    def __init__(self) -> None:
        super().__init__()
        self.epc_uri = None


class TagEncodable:
    def __init__(self) -> None:
        super().__init__()
        self._base64 = None
        self._binary = None
        self._hex = None
        self._tag_uri = None

    def tag_uri(self, **kwargs) -> str:
        raise NotImplementedError

    def binary(self, **kwargs) -> str:
        raise NotImplementedError

    def hex(self, **kwargs) -> str:
        binary = self.binary(**kwargs)

        padding = (16 - (len(binary) % 16)) % 16
        padded_binary = f"{binary:<0{len(binary) + padding}}"

        return f"{int(padded_binary, 2):X}"

    def base64(self, **kwargs) -> str:
        hex_string = self.hex(**kwargs)

        return hex_to_base64(hex_string)

    def from_binary(tag_binary_string: str) -> TagEncodable:
        raise NotImplementedError

    @classmethod
    def from_hex(cls, tag_hex_string: str) -> TagEncodable:
        return cls.from_binary(hex_to_binary(tag_hex_string))

    @classmethod
    def from_base64(cls, tag_hex_string: str) -> TagEncodable:
        return cls.from_binary(hex_to_base64(tag_hex_string))

class GS1Keyed:
    def __init__(self) -> None:
        super().__init__()
        self._gs1_key = None

    def gs1_key(self, *args, **kwargs) -> str:
        raise NotImplementedError
