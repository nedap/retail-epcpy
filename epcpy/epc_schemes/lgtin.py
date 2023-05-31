from __future__ import annotations

import re
from enum import IntEnum

from epcpy.epc_schemes.base_scheme import GS1Keyed
from epcpy.utils.common import (
    ConvertException,
    calculate_checksum,
    replace_uri_escapes,
    revert_uri_escapes,
    verify_gs3a3_component,
)
from epcpy.utils.regex import LGTIN_CLASS, LGTIN_GS1_ELEMENT_STRING

LGTIN_CLASS_REGEX = re.compile(LGTIN_CLASS)


class GTIN_TYPE(IntEnum):
    GTIN8 = (8,)
    GTIN12 = (12,)
    GTIN13 = (13,)
    GTIN14 = 14


class LGTIN(GS1Keyed):
    """LGTIN EPC scheme implementation.

    LGTIN pure identities are of the form:
        urn:epc:class:lgtin:<CompanyPrefix>.<ItemRefAndIndicator>.<Lot>

    Example:
        urn:epc:class:lgtin:061414.0123456.xyz3311cba

    This class can be created using EPC pure identities via its constructor, or using:
        - LGTIN.from_gs1_element_string

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
    """

    gs1_element_string_regex = re.compile(LGTIN_GS1_ELEMENT_STRING)

    def __init__(self, epc_class) -> None:
        super().__init__(epc_class)

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

        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )

        self._gtin = f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}".zfill(
            14
        )

    def gs1_key(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        """GS1 key belonging to this LGTIN instance

        Args:
            gtin_type (GTIN_TYPE, optional): What GTIN length to return.
                Defaults to GTIN_TYPE.GTIN14.

        Returns:
            str: GS1 key
        """
        return self.gtin(gtin_type=gtin_type)

    def gtin(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        """GTIN belonging to this LGTIN instance

        Args:
            gtin_type (GTIN_TYPE, optional): What GTIN length to return.
                Defaults to GTIN_TYPE.GTIN14.

        Raises:
            ConvertException: GTIN does not match given type

        Returns:
            str: GTIN
        """
        if gtin_type != GTIN_TYPE.GTIN14:
            if not self._gtin.startswith((14 - gtin_type) * "0"):
                raise ConvertException(message=f"Invalid GTIN{gtin_type}")

        return self._gtin[14 - gtin_type : 14]

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        gtin = self._gtin

        return f"(01){gtin}(10){self._lot}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> LGTIN:
        """Create a LGTIN instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: LGTIN GS1 element string invalid

        Returns:
            LGTIN: LGTIN scheme
        """
        if not LGTIN.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid LGTIN GS1 element string {gs1_element_string}"
            )

        _, digits, chars = re.split(f"\(.{{2}}\)", gs1_element_string)
        chars = revert_uri_escapes(chars)

        return cls(
            f"urn:epc:class:lgtin:{digits[1:company_prefix_length+1]}.{digits[0]}{digits[1+company_prefix_length:-1]}.{chars}"
        )
