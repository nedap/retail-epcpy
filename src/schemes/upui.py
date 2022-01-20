import re

from base_scheme import EPCSchemeNoTagURI
from common import (
    ConvertException,
    calculate_checksum,
    replace_uri_escapes,
    verify_gs3a3_component,
)
from regex import UPUI_URI

UPUI_URI_REGEX = re.compile(UPUI_URI)


class UPUI(EPCSchemeNoTagURI):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not UPUI_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid UPUI URI {epc_uri}")

        company_prefix, item_ref, *tpx = ":".join(epc_uri.split(":")[4:]).split(".")

        tpx = ".".join(tpx)
        verify_gs3a3_component(tpx)
        tpx = replace_uri_escapes(tpx)

        if not (1 <= len(tpx) <= 28):
            raise ConvertException(message=f"Incorrect TPX size")

        if len(f"{company_prefix}{item_ref}") != 13:
            raise ConvertException(
                message=f"Wrong company prefix + item ref size (!=13)"
            )

        check_digit = calculate_checksum(f"{item_ref[0]}{company_prefix}{item_ref[1:]}")

        self.epc_uri = epc_uri
        self._gs1_element_string = (
            f"(01){item_ref[0]}{company_prefix}{item_ref[1:]}{check_digit}(235){tpx}"
        )

    def gs1_element_string(self) -> str:
        return self._gs1_element_string
