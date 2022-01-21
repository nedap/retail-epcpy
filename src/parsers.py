import re

from base_scheme import EPCScheme
from common import BinaryHeaders, ConvertException, base64_to_hex, hex_to_binary
from converters import BINARY_CONVERTERS, TAG_CONVERTERS, URI_TO_SCHEME
from regex import TAG_URI

TAG_URI_REGEX = re.compile(TAG_URI)


def binary_to_epc_tag_uri(binary: str) -> str:
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


def binary_to_epc_pure_identity(binary: str) -> str:
    epc_tag_uri = binary_to_epc_tag_uri(binary)

    return epc_tag_uri_to_pure_identity_uri(epc_tag_uri)


def binary_to_epc_scheme(binary: str) -> EPCScheme:
    epc_pure_identity_uri = binary_to_epc_pure_identity(binary)
    return URI_TO_SCHEME(epc_pure_identity_uri.split(":")[3])(epc_pure_identity_uri)


def binary_to_gs1_key(binary: str) -> str:
    scheme = binary_to_epc_scheme(binary)
    return scheme.gs1_key()


def hex_to_epc_tag_uri(hex_string: str) -> str:
    binary = hex_to_binary(hex_string)

    return binary_to_epc_tag_uri(binary)


def hex_to_epc_pure_identity(hex_string: str) -> str:
    binary = hex_to_binary(hex_string)

    return binary_to_epc_pure_identity(binary)


def base64_to_epc_tag_uri(base64_string: str) -> str:
    hex_string = base64_to_hex(base64_string)

    return hex_to_epc_tag_uri(hex_string)


def base64_to_epc_pure_identity(base64_string: str) -> str:
    hex_string = base64_to_hex(base64_string)

    return hex_to_epc_pure_identity(hex_string)


def epc_tag_uri_to_pure_identity_uri(epc_tag_uri: str) -> str:
    if not TAG_URI_REGEX.match(epc_tag_uri):
        raise ConvertException(message=f"Invalid EPC tag URI {epc_tag_uri}")

    epc_scheme = epc_tag_uri.split(":")[3]
    value = TAG_CONVERTERS[epc_scheme](epc_tag_uri)

    return f"urn:epc:id:{epc_scheme.split('-')[0]}:{value}"
