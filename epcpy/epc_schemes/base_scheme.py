from __future__ import annotations

import re
from typing import Any, Dict

from epcpy.utils.common import ConvertException, hex_to_base64, hex_to_binary
from epcpy.utils.regex import TAG_URI


class EPCScheme:
    """Base class for EPC schemes

    Attributes:
        epc_uri (str): The EPC pure identity URI
    """
    def __init__(self) -> None:
        super().__init__()
        self.epc_uri = None

    @classmethod
    def from_epc_uri(cls, epc_uri: str) -> EPCScheme:
        """Instantiate an EPCScheme class from an EPC pure identity URI.

        Args:
            epc_uri (str): EPC pure identity URI.

        Returns:
            EPCScheme: Instance of EPCScheme class
        """
        return cls(epc_uri)


class TagEncodable:
    """Base class for tag encodable EPCSchemes

    Attributes:
        tag_uri (str): The EPC tag URI
        binary (str): Binary representation of the EPC tag URI
        hex (str): Hexadecimal representation of the EPC tag URI
        base64 (str): Base64 representation of the EPC tag URI
    """
    TAG_URI_REGEX = re.compile(TAG_URI)
    TAG_URI_PREFIX = "urn:epc:tag:"

    def __init__(self) -> None:
        super().__init__()
        self._base64 = None
        self._binary = None
        self._hex = None
        self._tag_uri = None

    def tag_uri(self, **kwargs) -> str:
        """Return the tag URI of the tag encodable

        Raises:
            NotImplementedError: Method not implemented by default.

        Returns:
            str: The tag URI.
        """
        raise NotImplementedError

    def binary(self, **kwargs) -> str:
        """Return the binary representation of the tag encodable

        Raises:
            NotImplementedError: Method not implemented by default.

        Returns:
            str: The binary representation.
        """
        raise NotImplementedError

    def hex(self, **kwargs) -> str:
        """Return the hexadecimal representation of the tag encodable

        Returns:
            str: The hexadecimal representation.
        """
        binary = self.binary(**kwargs)

        padding = (16 - (len(binary) % 16)) % 16
        padded_binary = f"{binary:<0{len(binary) + padding}}"

        return f"{int(padded_binary, 2):X}"

    def base64(self, **kwargs) -> str:
        """Return the base64 representation of the tag encodable

        Returns:
            str: The base64 representation.
        """
        hex_string = self.hex(**kwargs)

        return hex_to_base64(hex_string)

    def from_binary(tag_binary_string: str) -> TagEncodable:
        """Instantiate a TagEncodable class from a binary string.

        Args:
            tag_binary_string (str): Binary representation of a tag URI.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        raise NotImplementedError

    @classmethod
    def from_hex(cls, tag_hex_string: str) -> TagEncodable:
        """Instantiate a TagEncodable class from a hexidecimal string.

        Args:
            tag_hex_string (str): Hexidecimal representation of a tag URI.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        return cls.from_binary(hex_to_binary(tag_hex_string))

    @classmethod
    def from_base64(cls, tag_base64_string: str) -> TagEncodable:
        """Instantiate a TagEncodable class from a base64 string.

        Args:
            tag_base64_string (str): Base64 representation of a tag URI.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        return cls.from_binary(hex_to_base64(tag_base64_string))

    @classmethod
    def from_tag_uri(
        cls, epc_tag_uri: str, includes_filter: bool = True
    ) -> TagEncodable:
        """Instantiate a TagEncodable class from a tag URI.

        Args:
            epc_tag_uri (str): Tag URI.
            includes_filter (bool, optional): Whether a filter value is included in the tag URI.
                Defaults to True.

        Raises:
            ConvertException: Tag URI does not match any known tag URI schema.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        if not TagEncodable.TAG_URI_REGEX.match(epc_tag_uri):
            raise ConvertException(message=f"Invalid EPC tag URI {epc_tag_uri}")

        epc_scheme = epc_tag_uri.split(":")[3]

        if includes_filter:
            value = ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
        else:
            value = epc_tag_uri.split(":")[4]

        return cls(f"urn:epc:id:{epc_scheme.split('-')[0]}:{value}")

    @classmethod
    def header_to_schemes(cls) -> Dict[str, Any]:
        """Create dictionary of binary header -> binary coding scheme

        Returns:
            Dict[str, Any]: Dictionary mapping of binary header -> binary coding scheme
        """
        return {
            binary_header.value: cls.BinaryCodingScheme[binary_header.name]
            for binary_header in cls.BinaryHeader
        }


class GS1Keyed:
    """Base class for GS1 keyed EPCSchemes

    Attributes:
        gs1_key (str): GS1 key of the EPC pure identity
    """
    def __init__(self) -> None:
        super().__init__()
        self._gs1_key = None

    def gs1_key(self, *args, **kwargs) -> str:
        """GS1 key of the given EPC scheme

        Raises:
            NotImplementedError: not implemented by default

        Returns:
            str: GS1 key
        """
        raise NotImplementedError
