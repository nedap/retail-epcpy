import re

from epcpy.epc_schemes.base_scheme import EPCScheme
from epcpy.utils.common import (
    ConvertException,
    calculate_checksum,
    replace_uri_escapes,
    verify_gs3a3_component,
)
from epcpy.utils.regex import UPUI_URI

UPUI_URI_REGEX = re.compile(UPUI_URI)


class UPUI(EPCScheme):
    """UPUI EPC scheme implementation.

    UPUI pure identities are of the form:
        urn:epc:id:upui:<CompanyPrefix>.<ItemRefAndIndicator>.<TPX>

    Example:
        urn:epc:id:upui:1234567.089456.51qIgY)%3C%26Jp3*j7`SDB

    This class can be created using EPC pure identities via its constructor, or using:
        - UPUI.from_gs1_element_string

    Attributes:
        gs1_element_string (str): GS1 element string
    """

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not UPUI_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid UPUI URI {epc_uri}")

        self._company_pref, self._item_ref, *tpx = ":".join(
            epc_uri.split(":")[4:]
        ).split(".")

        tpx = ".".join(tpx)
        verify_gs3a3_component(tpx)
        self._tpx = replace_uri_escapes(tpx)

        if not (1 <= len(self._tpx) <= 28):
            raise ConvertException(message=f"Incorrect TPX size")

        if len(f"{self._company_pref}{self._item_ref}") != 13:
            raise ConvertException(
                message=f"Wrong company prefix + item ref size (!=13)"
            )

        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )

        self.epc_uri = epc_uri
        self._gs1_element_string = f"(01){self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}(235){self._tpx}"

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return self._gs1_element_string
