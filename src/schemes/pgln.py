import re

from base_scheme import EPCSchemeNoTagURI
from common import ConvertException, calculate_checksum
from regex import PGLN_URI

PGLN_URI_REGEX = re.compile(PGLN_URI)


class PGLN(EPCSchemeNoTagURI):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not PGLN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        if len(epc_uri.split(":")[4].replace(".", "")) != 12:
            raise ConvertException(
                message=f"Invalid component length {len(epc_uri.split(':')[4].replace('.', ''))}"
            )

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        company_prefix, party_ref = self.epc_uri.split(":")[4].split(".")

        check_digit = calculate_checksum(f"{company_prefix}{party_ref}")

        return f"(417){company_prefix}{party_ref}{check_digit}"
