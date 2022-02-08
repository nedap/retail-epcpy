import re

from epcpy.epc_schemes import *
from epcpy.epc_schemes.adi import ADI
from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from typing import List
from epcpy.epc_schemes.bic import BIC
from epcpy.epc_schemes.cpi import CPI
from epcpy.epc_schemes.sgtin import SGTIN
from epcpy.utils.common import (
    ConvertException,
    base64_to_hex,
    hex_to_binary,
)
from epcpy.utils.regex import TAG_URI

TAG_URI_REGEX = re.compile(TAG_URI)

EPC_SCHEMES: List[EPCScheme] = [ADI, BIC, CPI, SGTIN]  # todo
GS1_KEYED_CLASSES: List[GS1Keyed] = [SGTIN]
TAG_ENCODABLE_CLASSES: List[TagEncodable] = [SGTIN, ADI, CPI]  # todo


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


def binary_to_epc(binary: str) -> TagEncodable:

    for cls in TAG_ENCODABLE_CLASSES:
        try:
            return cls.from_binary(binary)
        except ConvertException as e:
            continue

    raise ConvertException(
        "Unable to find suitable TagEncodable class for given binary"
    )


def hex_to_epc(hex_string: str) -> TagEncodable:
    binary = hex_to_binary(hex_string)

    return binary_to_epc(binary)


def base64_to_epc(base64_string: str) -> TagEncodable:
    hex_string = base64_to_hex(base64_string)

    return hex_to_epc(hex_string)


def epc_tag_uri_to_pure_identity_uri(epc_tag_uri: str) -> str:
    pass
