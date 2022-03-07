import re
from typing import List

from epcpy.epc_pure_identities.adi import ADI
from epcpy.epc_pure_identities.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.epc_pure_identities.bic import BIC
from epcpy.epc_pure_identities.cpi import CPI
from epcpy.epc_pure_identities.gdti import GDTI
from epcpy.epc_pure_identities.giai import GIAI
from epcpy.epc_pure_identities.gid import GID
from epcpy.epc_pure_identities.ginc import GINC
from epcpy.epc_pure_identities.grai import GRAI
from epcpy.epc_pure_identities.gsin import GSIN
from epcpy.epc_pure_identities.gsrn import GSRN
from epcpy.epc_pure_identities.gsrnp import GSRNP
from epcpy.epc_pure_identities.imovn import IMOVN
from epcpy.epc_pure_identities.itip import ITIP
from epcpy.epc_pure_identities.pgln import PGLN
from epcpy.epc_pure_identities.sgcn import SGCN
from epcpy.epc_pure_identities.sgln import SGLN
from epcpy.epc_pure_identities.sgtin import SGTIN
from epcpy.epc_pure_identities.sscc import SSCC
from epcpy.epc_pure_identities.upui import UPUI
from epcpy.epc_pure_identities.usdod import USDOD
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
    identifier = epc_pure_identity_uri.split(":")[3]

    if identifier not in EPC_SCHEME_IDENTIFIERS:
        raise ConvertException("Unknown EPC URI")

    return EPC_SCHEME_IDENTIFIERS[identifier].from_epc_uri(epc_pure_identity_uri)


def epc_pure_identity_to_gs1_keyed(epc_pure_identity_uri: str) -> GS1Keyed:
    scheme = epc_pure_identity_to_scheme(epc_pure_identity_uri)

    if not isinstance(scheme, GS1Keyed):
        raise ConvertException(message="EPC URI has no GS1 Key")

    return scheme


def binary_to_epc(binary_string: str) -> TagEncodable:
    header = binary_string[:8]

    if header not in TAG_ENCODABLE_HEADERS:
        raise ConvertException("Unknown header")

    return TAG_ENCODABLE_HEADERS[header].from_binary(binary_string)


def hex_to_epc(hex_string: str) -> TagEncodable:
    binary = hex_to_binary(hex_string)

    return binary_to_epc(binary)


def base64_to_epc(base64_string: str) -> TagEncodable:
    hex_string = base64_to_hex(base64_string)

    return hex_to_epc(hex_string)
