import re

from epcpy.epc_pure_identities.base_scheme import EPCScheme
from epcpy.utils.common import (
    ConvertException,
    calculate_checksum,
    replace_uri_escapes,
    verify_gs3a3_component,
)
from epcpy.utils.regex import LGTIN_CLASS

LGTIN_CLASS_REGEX = re.compile(LGTIN_CLASS)


class LGTIN(EPCScheme):
    def __init__(self, epc_class) -> None:
        super().__init__()

        if not LGTIN_CLASS_REGEX.fullmatch(epc_class):
            raise ConvertException(message=f"Invalid LGTIN CLASS {epc_class}")

        self._company_pref, self._item_ref, *lot = ":".join(
            epc_class.split(":")[4:]
        ).split(".")

        self._lot = ".".join(lot)
        verify_gs3a3_component(self._lot)
        self._lot = replace_uri_escapes(self._lot)

        if not (6 <= len(self._company_pref) <= 12):
            raise ConvertException(
                message=f"Invalid company prefix length {len(self._company_pref)}"
            )

        if len(f"{self._company_pref}{self._item_ref}") != 13:
            raise ConvertException(
                message=f"Complete component length of invalid length (!=13)"
            )

        if not (1 <= len(self._lot) <= 20):
            raise ConvertException(message="Invalid lot length")

        self.epc_uri = epc_class

    def gs1_element_string(self) -> str:
        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )
        return f"(01){self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}(10){self._lot}"
