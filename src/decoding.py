import re

from common import BinaryHeaders, ConvertException, base64_to_hex, hex_to_binary
from regex import TAG_URI
from schemes.cpi import (
    binary_to_value_cpi96,
    binary_to_value_cpivar,
    tag_to_value_cpi96,
    tag_to_value_cpivar,
)
from schemes.gdti import (
    binary_to_value_gdti96,
    binary_to_value_gdti174,
    tag_to_value_gdti96,
    tag_to_value_gdti174,
)
from schemes.giai import (
    binary_to_value_giai96,
    binary_to_value_giai202,
    tag_to_value_giai96,
    tag_to_value_giai202,
)
from schemes.grai import (
    binary_to_value_grai96,
    binary_to_value_grai170,
    tag_to_value_grai96,
    tag_to_value_grai170,
)
from schemes.gsrn import binary_to_value_gsrn96, tag_to_value_gsrn96
from schemes.gsrnp import binary_to_value_gsrnp96, tag_to_value_gsrnp96
from schemes.sgcn import binary_to_value_sgcn96, tag_to_value_sgcn96
from schemes.sgln import (
    binary_to_value_sgln96,
    binary_to_value_sgln195,
    tag_to_value_sgln96,
    tag_to_value_sgln195,
)
from schemes.sgtin import (
    binary_to_value_sgtin96,
    binary_to_value_sgtin198,
    tag_to_value_sgtin96,
    tag_to_value_sgtin198,
)
from schemes.sscc import binary_to_value_sscc96, tag_to_value_sscc96

BINARY_CONVERTERS = {
    "sgtin-96": binary_to_value_sgtin96,
    "sgtin-198": binary_to_value_sgtin198,
    "sscc-96": binary_to_value_sscc96,
    "sgln-96": binary_to_value_sgln96,
    "sgln-195": binary_to_value_sgln195,
    "grai-96": binary_to_value_grai96,
    "grai-170": binary_to_value_grai170,
    "giai-96": binary_to_value_giai96,
    "giai-202": binary_to_value_giai202,
    "gsrn-96": binary_to_value_gsrn96,
    "gsrnp-96": binary_to_value_gsrnp96,
    "gdti-96": binary_to_value_gdti96,
    "gdti-174": binary_to_value_gdti174,
    "cpi-96": binary_to_value_cpi96,
    "cpi-var": binary_to_value_cpivar,
    "sgcn-96": binary_to_value_sgcn96,
}

TAG_CONVERTERS = {
    "sgtin-96": tag_to_value_sgtin96,
    "sgtin-198": tag_to_value_sgtin198,
    "sscc-96": tag_to_value_sscc96,
    "sgln-96": tag_to_value_sgln96,
    "sgln-195": tag_to_value_sgln195,
    "grai-96": tag_to_value_grai96,
    "grai-170": tag_to_value_grai170,
    "giai-96": tag_to_value_giai96,
    "giai-202": tag_to_value_giai202,
    "gsrn-96": tag_to_value_gsrn96,
    "gsrnp-96": tag_to_value_gsrnp96,
    "gdti-96": tag_to_value_gdti96,
    "gdti-174": tag_to_value_gdti174,
    "cpi-96": tag_to_value_cpi96,
    "cpi-var": tag_to_value_cpivar,
    "sgcn-96": tag_to_value_sgcn96,
}

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
