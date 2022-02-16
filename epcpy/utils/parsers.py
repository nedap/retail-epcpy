import re
from typing import List

from epcpy.epc_schemes.adi import ADI
from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.epc_schemes.bic import BIC
from epcpy.epc_schemes.cpi import CPI
from epcpy.epc_schemes.gdti import GDTI
from epcpy.epc_schemes.giai import GIAI
from epcpy.epc_schemes.gid import GID
from epcpy.epc_schemes.grai import GRAI
from epcpy.epc_schemes.gsrn import GSRN
from epcpy.epc_schemes.gsrnp import GSRNP
from epcpy.epc_schemes.itip import ITIP
from epcpy.epc_schemes.sgcn import SGCN
from epcpy.epc_schemes.sgln import SGLN
from epcpy.epc_schemes.sgtin import SGTIN
from epcpy.epc_schemes.sscc import SSCC
from epcpy.epc_schemes.usdod import USDOD
from epcpy.utils.common import ConvertException, base64_to_hex, hex_to_binary
from epcpy.utils.regex import TAG_URI

TAG_URI_REGEX = re.compile(TAG_URI)

EPC_SCHEMES: List[EPCScheme] = [ADI, BIC, CPI, SGTIN]  # TODO
GS1_KEYED_CLASSES: List[GS1Keyed] = [SGTIN]  # TODO
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


def epc_pure_identity_to_scheme(epc_pure_identity_uri: str) -> EPCScheme:

    for cls in EPC_SCHEMES:
        try:
            return cls.from_epc_uri(epc_pure_identity_uri)
        except:
            continue

    raise ConvertException(
        "Unable to find suitable EPCScheme class for given uri string"
    )


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
