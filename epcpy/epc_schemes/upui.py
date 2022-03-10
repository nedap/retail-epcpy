import re

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed
from epcpy.utils.common import (
    ConvertException,
    NoGS1KeyException,
    calculate_checksum,
    replace_uri_escapes,
    revert_uri_escapes,
    verify_gs3a3_component,
)
from epcpy.utils.regex import UPUI_GS1_ELEMENT_STRING, UPUI_URI

UPUI_URI_REGEX = re.compile(UPUI_URI)
UPUI_GS1_ELEMENT_STRING_REGEX = re.compile(UPUI_GS1_ELEMENT_STRING)


class UPUI(EPCScheme, GS1Keyed):
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

        self.epc_uri = epc_uri

    def gs1_key(self) -> None:
        raise NoGS1KeyException(
            message="UPUI has no GS1 key, only a GS1 element string"
        )

    def gs1_element_string(self) -> str:
        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )
        return f"(01){self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}(235){self._tpx}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GS1Keyed:
        if not UPUI_GS1_ELEMENT_STRING_REGEX.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid UPUI GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[4:18]
        chars = gs1_element_string[23:]
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:id:upui:{digits[1:1+company_prefix_length]}.{digits[0]}{digits[1+company_prefix_length:-1]}.{chars}"
        )
