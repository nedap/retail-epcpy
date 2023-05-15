from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    parse_header_and_truncate_binary,
    str_to_binary,
)
from epcpy.utils.regex import GID_URI

GID_URI_REGEX = re.compile(GID_URI)


class GID(TagEncodable):
    """GID EPC scheme implementation.

    GID pure identities are of the form:
        urn:epc:id:gid:<ManagerNumber>.<ObjectClass>.<SerialNumber>

    Example:
        urn:epc:id:gid:95100000.12345.400

    This class can be created using EPC pure identities via its constructor, or using:
        - GID.from_binary
        - GID.from_hex
        - GID.from_base64
        - GID.from_tag_uri

    Attributes:
        tag_uri (str): Tag URI
        binary (str): Binary representation
    """

    class BinaryCodingScheme(Enum):
        GID_96 = "gid-96"

    class BinaryHeader(Enum):
        GID_96 = "00110101"

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not GID_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GID URI {epc_uri}")

        self._manager, self._object, self._serial = epc_uri.split(":")[4].split(".")

        if int(self._manager) >= pow(2, 28):
            raise ConvertException(message=f"Manager out of range: (max: {pow(2, 28)})")

        if int(self._object) >= pow(2, 24):
            raise ConvertException(message=f"Object out of range: (max: {pow(2, 24)})")

        if int(self._serial) >= pow(2, 36) or (
            len(self._serial) > 1 and self._serial[0] == "0"
        ):
            raise ConvertException(message=f"Serial out of range: (max: {pow(2, 36)})")

        self.epc_uri = epc_uri

    def tag_uri(
        self,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.GID_96,
    ) -> str:
        """Return the tag URI belonging to this GID with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GIDFilterValue): Filter value

        Returns:
            str: Tag URI
        """
        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{self._manager}.{self._object}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme = BinaryCodingScheme.GID_96,
    ) -> str:
        """Return the binary representation belonging to this GID with the provided binary coding scheme and filter value.

        Args:
            binary_coding_scheme (BinaryCodingScheme): Coding scheme
            filter_value (GIDFilterValue): Filter value

        Returns:
            str: binary representation
        """
        header = GID.BinaryHeader[binary_coding_scheme.name].value
        manager_binary = str_to_binary(self._manager, 28)
        object_binary = str_to_binary(self._object, 24)
        serial_binary = str_to_binary(self._serial, 36)

        _binary = header + manager_binary + object_binary + serial_binary
        return _binary

    @classmethod
    def from_tag_uri(cls, epc_tag_uri: str, includes_filter=False):
        """Create a GID instance from a tag URI

        Args:
            epc_tag_uri (str): GID tag URI
            includes_filter (bool, optional): Whether this scheme contains a filter.
                Defaults to False.

        Returns:
            GID: GID instance
        """
        return super(GID, cls).from_tag_uri(
            epc_tag_uri, includes_filter=includes_filter
        )

    @classmethod
    def from_binary(cls, binary_string: str) -> GID:
        """Create an GID instance from a binary string

        Args:
            binary_string (str): binary representation of an GID

        Returns:
            GID: GID instance
        """
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        manager_binary = truncated_binary[8:36]
        object_binary = truncated_binary[36:60]
        serial_binary = truncated_binary[60:]

        manager_string = binary_to_int(manager_binary)
        object_string = binary_to_int(object_binary)
        serial_string = binary_to_int(serial_binary)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{manager_string}.{object_string}.{serial_string}",
            includes_filter=False,
        )
