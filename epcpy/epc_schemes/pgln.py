import re

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed
from epcpy.utils.common import ConvertException, calculate_checksum
from epcpy.utils.regex import PGLN_GS1_ELEMENT_STRING, PGLN_URI

PGLN_URI_REGEX = re.compile(PGLN_URI)
PGLN_GS1_ELEMENT_STRING_REGEX = re.compile(PGLN_GS1_ELEMENT_STRING)


class PGLN(EPCScheme, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not PGLN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid PGLN URI {epc_uri}")

        self._company_pref, self._party_ref = epc_uri.split(":")[4].split(".")

        if len(f"{self._company_pref}{self._party_ref}") != 12 or not (
            6 <= len(self._company_pref) <= 12
        ):
            raise ConvertException(message=f"Invalid EPC_URI")

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._party_ref}")

        self._pgln = f"{self._company_pref}{self._party_ref}{check_digit}"

    def gs1_key(self) -> str:
        return self._pgln

    def gs1_element_string(self) -> str:
        return f"(417){self._pgln}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GS1Keyed:
        if not PGLN_GS1_ELEMENT_STRING_REGEX.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid PGLN GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[5:]

        return cls(
            f"urn:epc:id:pgln:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}"
        )
