from epcpy.utils.common import hex_to_base64


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


class GS1Keyed:
    def __init__(self) -> None:
        super().__init__()
        self._gs1_key = None

    def gs1_key(self, *args, **kwargs) -> str:
        return self._gs1_key
