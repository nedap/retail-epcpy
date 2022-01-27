from epcpy.utils.common import hex_to_base64


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

    def binary(self, **kwargs) -> str:
        return self._binary

    def hex(self, **kwargs) -> str:
        binary = self.binary(**kwargs)

        padding = (16 - (len(binary) % 16)) % 16
        padded_binary = f"{binary:<0{len(binary) + padding}}"

        self._hex = f"{int(padded_binary, 2):X}"

        return self._hex

    def base64(self, **kwargs) -> str:
        hex_string = self.hex(**kwargs)

        self._base64 = hex_to_base64(hex_string)

        return self._base64


class EPCSchemeNoTagURI(EPCScheme):
    def __init__(self) -> None:
        super().__init__()

    def tag_uri(self, **kwargs) -> str:
        raise AttributeError(
            message="Tag URI scheme not available for provided EPC scheme"
        )

    def binary(self, **kwargs) -> str:
        raise AttributeError(
            message="Binary scheme not available for provided EPC scheme"
        )

    def hex(self, **kwargs) -> str:
        raise AttributeError(message="Hex scheme not available for provided EPC scheme")

    def base64(self, **kwargs) -> str:
        raise AttributeError(
            message="Base64 scheme not available for provided EPC scheme"
        )
