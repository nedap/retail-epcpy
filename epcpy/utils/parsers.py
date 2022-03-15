import re
from typing import List

from epcpy.epc_schemes.adi import ADI
from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.epc_schemes.bic import BIC
from epcpy.epc_schemes.cpi import CPI
from epcpy.epc_schemes.gdti import GDTI
from epcpy.epc_schemes.giai import GIAI
from epcpy.epc_schemes.gid import GID
from epcpy.epc_schemes.ginc import GINC
from epcpy.epc_schemes.grai import GRAI
from epcpy.epc_schemes.gsin import GSIN
from epcpy.epc_schemes.gsrn import GSRN
from epcpy.epc_schemes.gsrnp import GSRNP
from epcpy.epc_schemes.imovn import IMOVN
from epcpy.epc_schemes.itip import ITIP
from epcpy.epc_schemes.pgln import PGLN
from epcpy.epc_schemes.sgcn import SGCN
from epcpy.epc_schemes.sgln import SGLN
from epcpy.epc_schemes.sgtin import SGTIN
from epcpy.epc_schemes.sscc import SSCC
from epcpy.epc_schemes.upui import UPUI
from epcpy.epc_schemes.usdod import USDOD
from epcpy.utils.common import ConvertException, base64_to_hex, hex_to_binary
from epcpy.utils.regex import TAG_URI

TAG_URI_REGEX = re.compile(TAG_URI)

EPC_SCHEMES: List[EPCScheme] = [
    ADI,
    BIC,
    CPI,
    GDTI,
    GIAI,
    GID,
    GINC,
    GRAI,
    GSIN,
    GSRN,
    GSRNP,
    IMOVN,
    ITIP,
    PGLN,
    SGCN,
    SGLN,
    SGTIN,
    SSCC,
    UPUI,
    USDOD,
]
GS1_KEYED_CLASSES: List[GS1Keyed] = [
    GDTI,
    GIAI,
    GINC,
    GRAI,
    GSIN,
    GSRN,
    GSRNP,
    PGLN,
    SGCN,
    SGLN,
    SGTIN,
    SSCC,
]
TAG_ENCODABLE_CLASSES: List[TagEncodable] = [
    ADI,
    CPI,
    GDTI,
    GIAI,
    GID,
    GRAI,
    GSRN,
    GSRNP,
    ITIP,
    SGCN,
    SGLN,
    SGTIN,
    SSCC,
    USDOD,
]

TAG_ENCODABLE_HEADERS = {
    h.value: cls for cls in TAG_ENCODABLE_CLASSES for h in cls.BinaryHeader
}

EPC_SCHEME_IDENTIFIERS = {cls.__name__.lower(): cls for cls in EPC_SCHEMES}


def epc_pure_identity_to_scheme(epc_pure_identity_uri: str) -> EPCScheme:
    """Convert a EPC pure identity string into its schema class

    Args:
        epc_pure_identity_uri (str): EPC pure identity URI

    Raises:
        ConvertException: No matching class found for this URI

    Returns:
        EPCScheme: EPCScheme instance for this URI
    """
    identifier = epc_pure_identity_uri.split(":")[3]

    if identifier not in EPC_SCHEME_IDENTIFIERS:
        raise ConvertException("Unknown EPC URI")

    return EPC_SCHEME_IDENTIFIERS[identifier].from_epc_uri(epc_pure_identity_uri)


def epc_pure_identity_to_gs1_keyed(epc_pure_identity_uri: str) -> GS1Keyed:
    """Convert a EPC pure identity string into its GS1 keyed schema.

    Args:
        epc_pure_identity_uri (str): EPC pure identity URI

    Raises:
        ConvertException: Not a valid URI for a GS1 keyed schema

    Returns:
        GS1Keyed: GS1Keyed instance for this URI
    """
    scheme = epc_pure_identity_to_scheme(epc_pure_identity_uri)

    if not isinstance(scheme, GS1Keyed):
        raise ConvertException(message="EPC URI has no GS1 Key")

    return scheme


def binary_to_epc(binary_string: str) -> TagEncodable:
    """Binary string to TagEncodable class

    Args:
        binary_string (str): Binary string

    Raises:
        ConvertException: Binary header does not belong to valid TagEncodable class

    Returns:
        TagEncodable: TagEncodable class for this binary string
    """
    header = binary_string[:8]

    if header not in TAG_ENCODABLE_HEADERS:
        raise ConvertException("Unknown header")

    return TAG_ENCODABLE_HEADERS[header].from_binary(binary_string)


def hex_to_epc(hex_string: str) -> TagEncodable:
    """Hexadecimal string to TagEncodable class

    Args:
        hex_string (str): Hexadecimal string

    Returns:
        TagEncodable: TagEncodable class for this hexadecimal string
    """
    binary = hex_to_binary(hex_string)

    return binary_to_epc(binary)


def base64_to_epc(base64_string: str) -> TagEncodable:
    """Base64 string to TagEncodable class

    Args:
        base64_string (str): Base64 string

    Returns:
        TagEncodable: TagEncodable class for this base64 string
    """
    hex_string = base64_to_hex(base64_string)

    return hex_to_epc(hex_string)
