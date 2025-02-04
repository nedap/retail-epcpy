from __future__ import annotations

import re
from enum import Enum
from typing import Dict, Optional, Type, TypeVar

from epcpy.utils.common import ConvertException, base64_to_hex, hex_to_base64, hex_to_binary
from epcpy.utils.regex import TAG_URI

T_EPCScheme = TypeVar("T_EPCScheme", bound="EPCScheme")
T_GS1Element = TypeVar("T_GS1Element", bound="GS1Element")
T_TagEncodable = TypeVar("T_TagEncodable", bound="TagEncodable")


class EPCScheme:
    """Base class for EPC schemes

    Attributes:
        epc_uri (str): The EPC pure identity URI
    """

    def __init__(self, epc_uri: str) -> None:
        super().__init__()
        self.epc_uri = epc_uri

    def __eq__(self, other: object) -> bool:
        """Verify equality of two classes by validing if its an EPCScheme and whether the EPC URIs are equal.

        Args:
            other (object): Other object to compare against

        Returns:
            bool: Whether the other object is equal to this object
        """
        if not isinstance(other, EPCScheme):
            return False

        return self.epc_uri == other.epc_uri

    @classmethod
    def from_epc_uri(cls: Type[T_EPCScheme], epc_uri: str) -> EPCScheme:
        """Instantiate an EPCScheme class from an EPC pure identity URI.

        Args:
            epc_uri (str): EPC pure identity URI.

        Returns:
            EPCScheme: Instance of EPCScheme class
        """
        return cls(epc_uri)


class TagEncodable(EPCScheme):
    """Base class for tag encodable EPCSchemes

    Attributes:
        tag_uri (str): The EPC tag URI
        binary (str): Binary representation of the EPC tag URI
        hex (str): Hexadecimal representation of the EPC tag URI
        base64 (str): Base64 representation of the EPC tag URI
    """

    class BinaryCodingScheme(Enum):
        """Binary coding schemes for tag encodable EPC schemes"""

        pass

    class BinaryHeader(Enum):
        """Binary headers for tag encodable EPC schemes"""

        pass

    TAG_URI_REGEX = re.compile(TAG_URI)
    TAG_URI_PREFIX = "urn:epc:tag:"

    def __init__(self, epc_uri: str) -> None:
        super().__init__(epc_uri)

        self._base64: Optional[str] = None
        self._binary: Optional[str] = None
        self._hex: Optional[str] = None
        self._tag_uri: Optional[str] = None

    def tag_uri(self, *args, **kwargs) -> str:
        """Return the tag URI of the tag encodable

        Raises:
            NotImplementedError: Method not implemented by default.

        Returns:
            str: The tag URI.
        """
        raise NotImplementedError

    def binary(self, *args, **kwargs) -> str:
        """Return the binary representation of the tag encodable

        Raises:
            NotImplementedError: Method not implemented by default.

        Returns:
            str: The binary representation.
        """
        raise NotImplementedError

    def hex(self, *args, **kwargs) -> str:
        """Return the hexadecimal representation of the tag encodable

        Returns:
            str: The hexadecimal representation.
        """
        binary = self.binary(**kwargs)

        padding = (16 - (len(binary) % 16)) % 16
        padded_binary = f"{binary:<0{len(binary) + padding}}"

        return f"{int(padded_binary, 2):X}"

    def base64(self, *args, **kwargs) -> str:
        """Return the base64 representation of the tag encodable

        Returns:
            str: The base64 representation.
        """
        hex_string = self.hex(**kwargs)

        return hex_to_base64(hex_string)

    @classmethod
    def from_binary(
        cls: Type[T_TagEncodable], tag_binary_string: str
    ) -> T_TagEncodable:
        """Instantiate a TagEncodable class from a binary string.

        Args:
            tag_binary_string (str): Binary representation of a tag URI.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        raise NotImplementedError

    @classmethod
    def from_hex(cls: Type[T_TagEncodable], tag_hex_string: str) -> T_TagEncodable:
        """Instantiate a TagEncodable class from a hexidecimal string.

        Args:
            tag_hex_string (str): Hexidecimal representation of a tag URI.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        return cls.from_binary(hex_to_binary(tag_hex_string))

    @classmethod
    def from_base64(
        cls: Type[T_TagEncodable], tag_base64_string: str
    ) -> T_TagEncodable:
        """Instantiate a TagEncodable class from a base64 string.

        Args:
            tag_base64_string (str): Base64 representation of a tag URI.

        Returns:
            TagEncodable: Instance of TagEncodable class
        """
        return cls.from_hex(base64_to_hex(tag_base64_string))

    @classmethod
    def from_tag_uri(
        cls: Type[T_TagEncodable], epc_tag_uri: str, includes_filter: bool = True
    ) -> T_TagEncodable:
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
    def header_to_schemes(cls: Type[T_TagEncodable]) -> Dict[str, Enum]:
        """Create dictionary of binary header -> binary coding scheme

        Returns:
            Dict[str, Any]: Dictionary mapping of binary header -> binary coding scheme
        """
        return {
            binary_header.value: cls.BinaryCodingScheme[binary_header.name]
            for binary_header in cls.BinaryHeader
        }


class GS1Element(EPCScheme):
    gs1_element_string_regex: re.Pattern

    def __init__(self, epc_uri: str) -> None:
        super().__init__(epc_uri)

    def gs1_element_string(self, *args, **kwargs) -> str:
        """GS1 element string of the given EPC scheme

        Raises:
            NotImplementedError: not implemented by default

        Returns:
            str: GS1 element string
        """
        raise NotImplementedError

    @classmethod
    def from_gs1_element_string(
        cls: Type[T_GS1Element], gs1_element_string: str, company_prefix_length: int
    ) -> T_GS1Element:
        """Create a GS1Element instance from a GS1 element string and company prefix length.

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            NotImplementedError: Base class does not implement any scheme

        Returns:
            GS1Element: GS1Element instance
        """
        raise NotImplementedError


class GS1Keyed(GS1Element):
    def __init__(self, epc_uri: str) -> None:
        super().__init__(epc_uri)

    def gs1_key(self, *args, **kwargs) -> str:
        """GS1 key of the given EPC scheme

        Raises:
            NotImplementedError: not implemented by default

        Returns:
            str: GS1 key
        """
        raise NotImplementedError
