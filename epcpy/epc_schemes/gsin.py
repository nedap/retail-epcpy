from __future__ import annotations

import re

from epcpy.epc_schemes.base_scheme import GS1Keyed
from epcpy.utils.common import ConvertException
from epcpy.utils.regex import GSIN_GS1_ELEMENT_STRING, GSIN_URI

GSIN_URI_REGEX = re.compile(GSIN_URI)


def calculate_checksum(digits: str) -> int:
    """Alternative calculation of the checksum used solely by GSIN schemes.

    Args:
        digits (str): String of digits

    Returns:
        int: Check digit
    """
    digit_list = [int(d) for d in digits]
    odd, even = digit_list[1::2], digit_list[0::2]

    val1 = sum(odd)
    val2 = sum(even)

    checksum = (10 - ((3 * (val1) + (val2)) % 10)) % 10

    return checksum


class GSIN(GS1Keyed):
    """GSIN EPC scheme implementation.

    GSIN pure identities are of the form:
        urn:epc:id:gsin:<CompanyPrefix>.<ShipperReference>

    Example:
        urn:epc:id:gsin:0614141.123456789

    This class can be created using EPC pure identities via its constructor, or using:
        - GSIN.from_gs1_element_string

    Attributes:
        gs1_key (str): GS1 key
        gs1_element_string (str): GS1 element string
    """

    gs1_element_string_regex = re.compile(GSIN_GS1_ELEMENT_STRING)

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not GSIN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GSIN URI {epc_uri}")

        self._company_prefix, self._shipper_ref = epc_uri.split(":")[4].split(".")

        if len(f"{self._company_prefix}{self._shipper_ref}") != 16 or not (
            6 <= len(self._company_prefix) <= 12
        ):
            raise ConvertException(
                message=f"Invalid component length {len(epc_uri.split(':')[4].replace('.', ''))}"
            )

        self.epc_uri = epc_uri
        check_digit = calculate_checksum(f"{self._company_prefix}{self._shipper_ref}")

        self._gsin = f"{self._company_prefix}{self._shipper_ref}{check_digit}"

    def gs1_key(self) -> str:
        """Returns the GS1 key

        Returns:
            str: GS1 key
        """
        return self._gsin

    def gs1_element_string(self) -> str:
        """Returns the GS1 element string

        Returns:
            str: GS1 element string
        """
        return f"(402){self._gsin}"

    @classmethod
    def from_gs1_element_string(
        cls, gs1_element_string: str, company_prefix_length: int
    ) -> GSIN:
        """Create a GSIN instance from a GS1 element string and company prefix

        Args:
            gs1_element_string (str): GS1 element string
            company_prefix_length (int): Company prefix length

        Raises:
            ConvertException: GSIN GS1 element string invalid

        Returns:
            GSIN: GSIN scheme
        """
        if not GSIN.gs1_element_string_regex.fullmatch(gs1_element_string):
            raise ConvertException(
                message=f"Invalid GSIN GS1 element string {gs1_element_string}"
            )

        digits = gs1_element_string[5:-1]

        return cls(
            f"urn:epc:id:gsin:{digits[:company_prefix_length]}.{digits[company_prefix_length:]}"
        )
