import re
from typing import Dict, List, Optional, Type

from epcpy.epc_schemes import (
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
    LGTIN,
    PGLN,
    SGCN,
    SGLN,
    SGTIN,
    SSCC,
    UPUI,
    USDOD,
)
from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Element, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    base64_to_hex,
    binary_to_hex,
    hex_to_binary,
)
from epcpy.utils.regex import EPC_URI, GS1_ELEMENT_STRING, IDPAT_URI, TAG_URI

EPC_URI_REGEX = re.compile(EPC_URI)
GS1_ELEMENT_STRING_REGEX = re.compile(GS1_ELEMENT_STRING)
IDPAT_URI_REGEX = re.compile(IDPAT_URI)
TAG_URI_REGEX = re.compile(TAG_URI)

EPC_SCHEMES: List[Type[EPCScheme]] = [
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
    LGTIN,
    PGLN,
    SGCN,
    SGLN,
    SGTIN,
    SSCC,
    UPUI,
    USDOD,
]
GS1_KEYED_CLASSES: List[Type[GS1Keyed]] = [
    cls for cls in EPC_SCHEMES if issubclass(cls, GS1Keyed)
]
TAG_ENCODABLE_CLASSES: List[Type[TagEncodable]] = [
    cls for cls in EPC_SCHEMES if issubclass(cls, TagEncodable)
]

TAG_ENCODABLE_BINARY_HEADERS = {
    h.value: cls for cls in TAG_ENCODABLE_CLASSES for h in cls.BinaryHeader
}
TAG_ENCODABLE_HEX_HEADERS = {
    binary_to_hex(h.value): cls
    for cls in TAG_ENCODABLE_CLASSES
    for h in cls.BinaryHeader
}

GS1_ELEMENT_STRING_REGEX_TO_SCHEME: Dict[re.Pattern, Type[GS1Element]] = {
    cls.gs1_element_string_regex: cls
    for cls in EPC_SCHEMES
    if issubclass(cls, GS1Element)
}

EPC_SCHEME_IDENTIFIERS = {cls.__name__.lower(): cls for cls in EPC_SCHEMES}
TAG_ENCODABLE_SCHEME_IDENTIFIERS = {
    cls.__name__.lower(): cls for cls in TAG_ENCODABLE_CLASSES
}
GS1_KEYED_SCHEME_IDENTIFIERS = {cls.__name__.lower(): cls for cls in GS1_KEYED_CLASSES}


def get_gs1_key(
    source: str, company_prefix_length: Optional[int] = None, **kwargs
) -> str:
    """Get the GS1 key belonging to the source string.
    This method can identify and parse:
    - EPC pure identity URIs
    - EPC tag URIs
    - GS1 element strings (company_prefix_length should be provided)
    - IDPAT URIs
    - Binary strings
    - Hexadecimal strings

    Args:
        source (str): Source string
        company_prefix_length (int, optional): Company prefix length, required for gs1 element strings.
            Defaults to None.

    Raises:
        ConvertException: Source could not be converted to GS1 key

    Returns:
        str: GS1 key of source string
    """
    scheme = None

    if EPC_URI_REGEX.fullmatch(source):
        scheme = epc_pure_identity_to_scheme(source)
    elif GS1_ELEMENT_STRING_REGEX.fullmatch(source) and company_prefix_length:
        scheme = gs1_element_string_to_gs1_element(source, company_prefix_length)
    elif TAG_URI_REGEX.fullmatch(source):
        scheme = tag_uri_to_tag_encodable(source)
    elif IDPAT_URI_REGEX.fullmatch(source):
        scheme = _idpat_to_gs1_keyed_scheme(source)
    elif source[:8] in TAG_ENCODABLE_BINARY_HEADERS.keys():
        scheme = binary_to_tag_encodable(source)
    elif source[:2].upper() in TAG_ENCODABLE_HEX_HEADERS.keys():
        scheme = hex_to_tag_encodable(source)

    if not isinstance(scheme, GS1Keyed):
        raise ConvertException(
            message="Source could not be converted to proper GS1Keyed scheme"
        )

    return scheme.gs1_key(**kwargs)


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
    return epc_pure_identity_to_gs1_element(epc_pure_identity_uri).gs1_element_string()


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


def gs1_element_string_to_gs1_element(
    gs1_element_string: str, company_prefix_length: int
) -> GS1Element:
    """EPC gs1 element string to GS1Element class

    Args:
        gs1_element_string (str): GS1 element string

    Raises:
        ConvertException: Scheme is not GS1Element

    Returns:
        GS1Element: GS1Element class for this gs1 element string
    """
    for regex, scheme in GS1_ELEMENT_STRING_REGEX_TO_SCHEME.items():
        if regex.fullmatch(gs1_element_string):
            return scheme.from_gs1_element_string(
                gs1_element_string, company_prefix_length
            )

    raise ConvertException(message=f"Unknown GS1 element string: {gs1_element_string}")


ONE_ESCAPE_ALLOWED_SCHEMES = [
    cls.__name__.lower()
    for cls in [
        SGTIN,
        SGLN,
        GRAI,
        GDTI,
        CPI,
    ]
]


def _idpat_to_gs1_keyed_scheme(idpat: str) -> GS1Keyed:
    """Create a GS1Keyed scheme from an IDPAT URI
    Since an IDPAT can target a group of EPCs, the returned scheme should only be used for the GS1 key.

    Args:
        idpat (str): ID pattern URI

    Returns:
        GS1Keyed: GS1 keyed scheme
    """
    identifier = idpat.split(":")[3]

    if identifier not in GS1_KEYED_SCHEME_IDENTIFIERS:
        raise ConvertException(message="Unknown GS1Keyed identifier")

    # Create URI from idpat
    uri = idpat.replace("idpat", "id", 1)

    # URI already matches existing scheme
    if EPC_URI_REGEX.fullmatch(uri):
        return GS1_KEYED_SCHEME_IDENTIFIERS[identifier](uri)

    if identifier not in ONE_ESCAPE_ALLOWED_SCHEMES:
        raise ConvertException(message="URI exceeds maximum number of escaped patterns")

    # Create URI with dummy serial to create GS1 key
    dummy_uri = re.sub("\.\*$", ".0", uri, 1)
    if EPC_URI_REGEX.fullmatch(dummy_uri):
        return GS1_KEYED_SCHEME_IDENTIFIERS[identifier](dummy_uri)

    raise ConvertException(message="Could not create valid scheme from given id pat")


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

    if header not in TAG_ENCODABLE_BINARY_HEADERS:
        raise ConvertException(message="Unknown header")

    return TAG_ENCODABLE_BINARY_HEADERS[header].from_binary(binary_string)


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
