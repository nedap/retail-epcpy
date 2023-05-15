from __future__ import annotations

import re

from epcpy.epc_schemes.base_scheme import GS1Keyed
from epcpy.utils.common import ConvertException, calculate_checksum
from epcpy.utils.regex import PGLN_GS1_ELEMENT_STRING, PGLN_URI

PGLN_URI_REGEX = re.compile(PGLN_URI)


class PGLN(GS1Keyed):
    """PGLN EPC scheme implementation.

    PGLN pure identities are of the form:
        urn:epc:id:pgln:<CompanyPrefix>.<PartyReference>

    Example:
        urn:epc:id:pgln:1234567.89012

    This class can be created using EPC pure identities via its constructor, or using:
        - PGLN.from_gs1_element_string

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
    """

    gs1_element_string_regex = re.compile(PGLN_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

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
        """Returns the GS1 key

        Returns:
            str: GS1 key
        """
        return self._pgln

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(417){self._pgln}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> PGLN:
        """Create a PGLN instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: PGLN GS1 element string invalid

        Returns:
            PGLN: PGLN scheme
        """
        if not PGLN.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid PGLN GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[5:]

        return cls(
            f"urn:epc:id:pgln:{digits[:company_prefix_length]}.{digits[company_prefix_length:-1]}"
        )
