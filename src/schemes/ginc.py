import re

from base_scheme import EPCSchemeNoTagURI
from common import ConvertException, replace_uri_escapes, verify_gs3a3_component
from regex import GINC_URI

GINC_URI_REGEX = re.compile(GINC_URI)


class GINC(EPCSchemeNoTagURI):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GINC_URI_REGEX.match(epc_uri):
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
        return self._ginc

    def gs1_element_string(self) -> str:
        return f"(401){self._ginc}"
