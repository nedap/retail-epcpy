import re

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed
from epcpy.utils.common import (
    ConvertException,
    replace_uri_escapes,
    revert_uri_escapes,
    verify_gs3a3_component,
)
from epcpy.utils.regex import GINC_GS1_ELEMENT_STRING, GINC_URI

GINC_URI_REGEX = re.compile(GINC_URI)
GINC_GS1_ELEMENT_STRING_REGEX = re.compile(GINC_GS1_ELEMENT_STRING)


class GINC(EPCScheme, GS1Keyed):
    """GINC EPC scheme implementation.

    GINC pure identities are of the form:
        urn:epc:id:ginc:<CompanyPrefix>.<ConsignmentReference>

    Example:
        urn:epc:id:ginc:0614141.xyz3311cba

    This class can be created using EPC pure identities via its constructor, or using:
        - GINC.from_gs1_element_string

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
    """

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GINC_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GINC URI {epc_uri}")

        company_prefix, *consignment_reference = ":".join(epc_uri.split(":")[4:]).split(
            "."
        )

        consignment_reference = ".".join(consignment_reference)
        verify_gs3a3_component(consignment_reference)
        consignment_reference = replace_uri_escapes(consignment_reference)

        if not (6 <= len(company_prefix) <= 12):
            raise ConvertException(
                message=f"Invalid company prefix length {len(company_prefix)}"
            )

        if len(consignment_reference) == 0:
            raise ConvertException(message=f"Consignment reference too small")

        if len(f"{company_prefix}{consignment_reference}") > 30:
            raise ConvertException(message=f"Complete component length too large (>30)")

        self.epc_uri = epc_uri
        self._ginc = f"{company_prefix}{consignment_reference}"

    def gs1_key(self) -> str:
        """Returns the GS1 key

        Returns:
            str: GS1 key
        """
        return self._ginc

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(401){self._ginc}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GS1Keyed:
        if not GINC_GS1_ELEMENT_STRING_REGEX.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid GINC GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[5 : 5 + company_prefix_length]
        chars = gs1_element_string[5 + company_prefix_length :]
        chars = revert_uri_escapes(chars)

        return cls(f"urn:epc:id:ginc:{digits}.{chars}")
