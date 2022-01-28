import re

from epcpy.epc_schemes.base_scheme import EPCScheme
from epcpy.utils.common import BinaryHeaders, ConvertException, base64_to_hex, hex_to_binary
from epcpy.utils.converters import BINARY_CONVERTERS, TAG_CONVERTERS, URI_TO_SCHEME
from epcpy.utils.regex import TAG_URI

TAG_URI_REGEX = re.compile(TAG_URI)


def epc_pure_identity_to_scheme(epc_pure_identity_uri: str) -> EPCScheme:
    return URI_TO_SCHEME[epc_pure_identity_uri.split(":")[3]](epc_pure_identity_uri)


def epc_pure_identity_to_gs1_key(epc_pure_identity_uri: str) -> str:
    scheme = epc_pure_identity_to_scheme(epc_pure_identity_uri)

    return scheme.gs1_key()


def binary_to_epc_tag_uri(binary: str, ignore_exceptions=False) -> str:
    try:
        header = binary[:8]

        try:
            scheme = BinaryHeaders(header).name.replace("_", "-").lower()
        except ValueError:
            raise ConvertException(message=f"{header} is not a valid header")

        _, size = scheme.split("-")
        size = int(size) if size.isnumeric() else None

        if size and not size <= len(binary):
            raise ConvertException(
                message=f"Invalid binary size, expected (<=): {size} actual: {len(binary)}"
            )
        truncated_binary = binary[:size]

        value = BINARY_CONVERTERS[scheme](truncated_binary)

        return f"urn:epc:tag:{scheme}:{value}"
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def binary_to_epc_pure_identity(binary: str, ignore_exceptions=False) -> str:
    try:
        epc_tag_uri = binary_to_epc_tag_uri(binary)  # 20 s

        return epc_tag_uri_to_pure_identity_uri(epc_tag_uri)  # 13s
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def binary_to_epc_scheme(binary: str, ignore_exceptions=False) -> EPCScheme:
    try:
        epc_pure_identity_uri = binary_to_epc_pure_identity(binary)

        return epc_pure_identity_to_scheme(epc_pure_identity_uri)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def binary_to_gs1_key(binary: str, ignore_exceptions=False) -> str:
    try:
        scheme = binary_to_epc_scheme(binary)

        return scheme.gs1_key()
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def hex_to_epc_tag_uri(hex_string: str, ignore_exceptions=False) -> str:
    try:
        binary = hex_to_binary(hex_string)

        return binary_to_epc_tag_uri(binary)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def hex_to_epc_pure_identity(hex_string: str, ignore_exceptions=False) -> str:
    try:
        binary = hex_to_binary(hex_string)

        return binary_to_epc_pure_identity(binary)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def hex_to_gs1_key(hex_string: str, ignore_exceptions=False) -> str:
    try:
        binary = hex_to_binary(hex_string)

        return binary_to_gs1_key(binary)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def base64_to_epc_tag_uri(base64_string: str, ignore_exceptions=False) -> str:
    try:
        hex_string = base64_to_hex(base64_string)

        return hex_to_epc_tag_uri(hex_string)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def base64_to_epc_pure_identity(base64_string: str, ignore_exceptions=False) -> str:
    try:
        hex_string = base64_to_hex(base64_string)

        return hex_to_epc_pure_identity(hex_string)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def base64_to_gs1_key(base64_string: str, ignore_exceptions=False) -> str:
    try:
        hex_string = base64_to_hex(base64_string)

        return hex_to_gs1_key(hex_string)
    except ConvertException:
        if ignore_exceptions:
            return None
        raise


def epc_tag_uri_to_pure_identity_uri(epc_tag_uri: str, ignore_exceptions=False) -> str:
    try:
        if not TAG_URI_REGEX.match(epc_tag_uri):
            raise ConvertException(message=f"Invalid EPC tag URI {epc_tag_uri}")

        epc_scheme = epc_tag_uri.split(":")[3]
        value = TAG_CONVERTERS[epc_scheme](epc_tag_uri)

        return f"urn:epc:id:{epc_scheme.split('-')[0]}:{value}"
    except ConvertException:
        if ignore_exceptions:
            return None
        raise
