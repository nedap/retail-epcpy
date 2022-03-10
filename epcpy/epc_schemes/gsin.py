import re

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed
from epcpy.utils.common import ConvertException
from epcpy.utils.regex import GSIN_URI

GSIN_URI_REGEX = re.compile(GSIN_URI)


def calculate_checksum(digits: str) -> int:
    digits = [int(d) for d in digits]
    odd, even = digits[1::2], digits[0::2]

    val1 = sum(odd)
    val2 = sum(even)

    checksum = (10 - ((3 * (val1) + (val2)) % 10)) % 10

    return checksum


class GSIN(EPCScheme, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

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
        return self._gsin

    def gs1_element_string(self) -> str:
        return f"(402){self._gsin}"
