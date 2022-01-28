import re

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed
from epcpy.utils.common import ConvertException, calculate_checksum
from epcpy.utils.regex import PGLN_URI

PGLN_URI_REGEX = re.compile(PGLN_URI)


class PGLN(EPCScheme, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not PGLN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid PGLN URI {epc_uri}")

        if len(epc_uri.split(":")[4].replace(".", "")) != 12:
            raise ConvertException(
                message=f"Invalid component length {len(epc_uri.split(':')[4].replace('.', ''))}"
            )

        self.epc_uri = epc_uri

        company_prefix, party_ref = self.epc_uri.split(":")[4].split(".")
        check_digit = calculate_checksum(f"{company_prefix}{party_ref}")

        self._pgln = f"{company_prefix}{party_ref}{check_digit}"

    def gs1_key(self) -> str:
        return self._pgln

    def gs1_element_string(self) -> str:
        return f"(417){self._pgln}"
