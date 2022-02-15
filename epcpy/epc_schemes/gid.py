from __future__ import annotations
import re

from epcpy.epc_schemes.base_scheme import EPCScheme, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    parse_header_and_truncate_binary,
    str_to_binary,
)
from enum import Enum
from epcpy.utils.regex import GID_URI

GID_URI_REGEX = re.compile(GID_URI)


class GID(EPCScheme, TagEncodable):
    class BinaryCodingScheme(Enum):
        GID_96 = "gid-96"

    class BinaryHeader(Enum):
        GID_96 = "00110101"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GID_URI_REGEX.match(epc_uri):
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
        binary_coding_scheme: GID.BinaryCodingScheme.GID_96 = BinaryCodingScheme.GID_96,
    ) -> str:
        return f"urn:epc:tag:{binary_coding_scheme.value}:{self._manager}.{self._object}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: GID.BinaryCodingScheme.GID_96 = BinaryCodingScheme.GID_96,
    ) -> str:

        header = GID.BinaryHeader[binary_coding_scheme.name].value
        manager_binary = str_to_binary(self._manager, 28)
        object_binary = str_to_binary(self._object, 24)
        serial_binary = str_to_binary(self._serial, 36)

        _binary = header + manager_binary + object_binary + serial_binary
        return _binary

    @classmethod
    def from_binary(cls, binary_string: str) -> GID:
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
        print(manager_string)
        print(object_string)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{manager_string}.{object_string}.{serial_string}"
        )
