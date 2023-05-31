from __future__ import annotations

import re

from epcpy.epc_schemes.base_scheme import GS1Element
from epcpy.utils.common import (
    ConvertException,
    calculate_checksum,
    replace_uri_escapes,
    revert_uri_escapes,
    verify_gs3a3_component,
)
from epcpy.utils.regex import UPUI_GS1_ELEMENT_STRING, UPUI_URI

UPUI_URI_REGEX = re.compile(UPUI_URI)


class UPUI(GS1Element):
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

    gs1_element_string_regex = re.compile(UPUI_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not UPUI_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid UPUI URI {epc_uri}")

        self._company_pref, self._item_ref, *tpx_components = ":".join(
            epc_uri.split(":")[4:]
        ).split(".")

        tpx = ".".join(tpx_components)
        verify_gs3a3_component(tpx)
        self._tpx = replace_uri_escapes(tpx)

        if not (1 <= len(self._tpx) <= 28):
            raise ConvertException(message=f"Incorrect TPX size")

        if len(f"{self._company_pref}{self._item_ref}") != 13:
            raise ConvertException(
                message=f"Wrong company prefix + item ref size (!=13)"
            )

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )
        return f"(01){self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}(235){self._tpx}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> UPUI:
        """Create a UPUI instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: UPUI GS1 element string invalid

        Returns:
            UPUI: UPUI scheme
        """
        if not UPUI.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid UPUI GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[4:18]
        chars = gs1_element_string[23:]
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:upui:{digits[1:1+company_prefix_length]}.{digits[0]}{digits[1+company_prefix_length:-1]}.{chars}"
        )
