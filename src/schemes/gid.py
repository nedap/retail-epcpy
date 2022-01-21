import re

from base_scheme import EPCScheme
from common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    str_to_binary,
)
from regex import GID_URI

GID_URI_REGEX = re.compile(GID_URI)


class GID(EPCScheme):
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

    def tag_uri(self) -> str:
        if self._tag_uri:
            return self._tag_uri

        scheme = BinaryCodingSchemes.GID_96.value

        self._tag_uri = (
            f"urn:epc:tag:{scheme}:{self._manager}.{self._object}.{self._serial}"
        )

        return self._tag_uri

    def binary(self) -> str:
        if self._binary:
            return self._binary

        self.tag_uri()

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()

        header = BinaryHeaders[scheme].value
        manager_binary = str_to_binary(self._manager, 28)
        object_binary = str_to_binary(self._object, 24)
        serial_binary = str_to_binary(self._serial, 36)

        self._binary = header + manager_binary + object_binary + serial_binary
        return self._binary


def binary_to_value_gid96(truncated_binary: str) -> str:
    manager_binary = truncated_binary[8:36]
    object_binary = truncated_binary[36:60]
    serial_binary = truncated_binary[60:]

    manager_string = binary_to_int(manager_binary)
    object_string = binary_to_int(object_binary)
    serial_string = binary_to_int(serial_binary)

    return f"{manager_string}.{object_string}.{serial_string}"


def tag_to_value_gid96(epc_tag_uri: str) -> str:
    return epc_tag_uri.split(":")[4]
