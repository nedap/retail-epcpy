from typing import Any

from common import BinaryCodingSchemes, hex_to_base64


class EPCScheme:
    def __init__(self) -> None:
        self._base64 = None
        self._binary = None
        self._hex = None
        self._tag_uri = None
        self._gs1_key = None

        self.epc_uri = None

    def gs1_key(self, *args, **kwargs) -> str:
        return self._gs1_key

    def binary(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> Any:
        return self._binary

    def hex(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        if self._hex:
            return self._hex

        if binary_coding_scheme and filter_value:
            binary = self.binary(
                binary_coding_scheme=binary_coding_scheme, filter_value=filter_value
            )
        elif binary_coding_scheme:
            binary = self.binary(binary_coding_scheme=binary_coding_scheme)
        elif filter_value:
            binary = self.binary(filter_value=filter_value)
        else:
            binary = self.binary()

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


class EPCSchemeNoTagURI(EPCScheme):
    def __init__(self) -> None:
        super().__init__()

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        raise AttributeError(
            message="Tag URI scheme not available for provided EPC scheme"
        )

    def binary(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        raise AttributeError(
            message="Binary scheme not available for provided EPC scheme"
        )

    def hex(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        raise AttributeError(message="Hex scheme not available for provided EPC scheme")

    def base64(
        self, binary_coding_scheme: BinaryCodingSchemes = None, filter_value: Any = None
    ) -> str:
        raise AttributeError(
            message="Base64 scheme not available for provided EPC scheme"
        )
