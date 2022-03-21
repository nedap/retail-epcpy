import logging
import re
from typing import Any, Callable, List

from epcpy.epc_schemes.adi import ADI
from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Element, GS1Keyed, TagEncodable
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
    cls for cls in EPC_SCHEMES if issubclass(cls, GS1Keyed)
]
TAG_ENCODABLE_CLASSES: List[TagEncodable] = [
    cls for cls in EPC_SCHEMES if issubclass(cls, TagEncodable)
]

TAG_ENCODABLE_HEADERS = {
    h.value: cls for cls in TAG_ENCODABLE_CLASSES for h in cls.BinaryHeader
}

EPC_SCHEME_IDENTIFIERS = {cls.__name__.lower(): cls for cls in EPC_SCHEMES}
TAG_ENCODABLE_SCHEME_IDENTIFIERS = {
    cls.__name__.lower(): cls for cls in TAG_ENCODABLE_CLASSES
}


def ignore_errors(func: Callable[..., Any], *args, **kwargs) -> Any:
    """Helper function to support large scale conversions where its fine to have some invalid URIs.
    Does log the exception on debug level.

    Args:
        func (Callable[..., Any]): Function to execute

    Returns:
        Any: Value from the provided function
    """
    try:
        return func(*args, **kwargs)
    except ConvertException as e:
        logging.debug(e)
        return None


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
        raise ConvertException(message="Unknown EPC URI")

    return EPC_SCHEME_IDENTIFIERS[identifier].from_epc_uri(epc_pure_identity_uri)


def epc_pure_identity_to_gs1_element(epc_pure_identity_uri: str) -> GS1Element:
    """Convert a EPC pure identity string into its GS1 element schema.

    Args:
        epc_pure_identity_uri (str): EPC pure identity URI

    Raises:
        ConvertException: Not a valid URI for a GS1 element schema

    Returns:
        GS1Element: GS1Element instance for this URI
    """
    scheme = epc_pure_identity_to_scheme(epc_pure_identity_uri)

    if not isinstance(scheme, GS1Element):
        raise ConvertException(message="EPC URI has no GS1 Element")

    return scheme


def epc_pure_identity_to_gs1_element_string(epc_pure_identity_uri: str) -> str:
    """Convert a EPC pure identity string into a GS1 element string.

    Args:
        epc_pure_identity_uri (str): EPC pure identity URI

    Returns:
        str: GS1 element string for this URI
    """
    return epc_pure_identity_to_gs1_keyed(epc_pure_identity_uri).gs1_element_string()


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


def epc_pure_identity_to_gs1_key(epc_pure_identity_uri: str, **kwargs) -> str:
    """Convert a EPC pure identity string into a GS1 key.

    Args:
        epc_pure_identity_uri (str): EPC pure identity URI

    Returns:
        str: GS1 key for this URI
    """
    return epc_pure_identity_to_gs1_keyed(epc_pure_identity_uri).gs1_key(**kwargs)


def epc_pure_identity_to_tag_encodable(epc_pure_identity_uri: str) -> TagEncodable:
    """Convert a EPC pure identity string into a TagEncodable scheme

    Args:
        epc_pure_identity_uri (str): EPC pure identity URI

    Raises:
        ConvertException: Scheme is not TagEncodable

    Returns:
        TagEncodable: TagEncodable instance of the URI
    """
    scheme = epc_pure_identity_to_scheme(epc_pure_identity_uri)

    if not isinstance(scheme, TagEncodable):
        raise ConvertException(message="EPC URI is not tag encodable")

    return scheme


def tag_uri_to_tag_encodable(epc_tag_uri: str) -> TagEncodable:
    """EPC tag URI to TagEncodable class

    Args:
        epc_tag_uri (str): EPC tag URI

    Returns:
        TagEncodable: TagEncodable class for this tag URI
    """
    identifier = epc_tag_uri.split(":")[3].split("-")[0]

    if identifier not in TAG_ENCODABLE_SCHEME_IDENTIFIERS:
        raise ConvertException(message="Unknown TagEncodable scheme identifier")

    return TAG_ENCODABLE_SCHEME_IDENTIFIERS[identifier].from_tag_uri(epc_tag_uri)


def binary_to_tag_encodable(binary_string: str) -> TagEncodable:
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
        raise ConvertException(message="Unknown header")

    return TAG_ENCODABLE_HEADERS[header].from_binary(binary_string)


def hex_to_tag_encodable(hex_string: str) -> TagEncodable:
    """Hexadecimal string to TagEncodable class

    Args:
        hex_string (str): Hexadecimal string

    Returns:
        TagEncodable: TagEncodable class for this hexadecimal string
    """
    binary = hex_to_binary(hex_string)

    return binary_to_tag_encodable(binary)


def base64_to_tag_encodable(base64_string: str) -> TagEncodable:
    """Base64 string to TagEncodable class

    Args:
        base64_string (str): Base64 string

    Returns:
        TagEncodable: TagEncodable class for this base64 string
    """
    hex_string = base64_to_hex(base64_string)

    return hex_to_tag_encodable(hex_string)
