import re

from base_scheme import EPCSchemeNoTagURI
from common import ConvertException
from regex import GSIN_URI

GSIN_URI_REGEX = re.compile(GSIN_URI)


def calculate_checksum(digits: str) -> int:
    digits = [int(d) for d in digits]
    odd, even = digits[1::2], digits[0::2]

    val1 = sum(odd)
    val2 = sum(even)

    checksum = (10 - ((3 * (val1) + (val2)) % 10)) % 10

    return checksum


class GSIN(EPCSchemeNoTagURI):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GSIN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        if len(epc_uri.split(":")[4].replace(".", "")) != 16:
            raise ConvertException(
                message=f"Invalid component length {len(epc_uri.split(':')[4].replace('.', ''))}"
            )

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        company_prefix, shipper_ref = self.epc_uri.split(":")[4].split(".")

        check_digit = calculate_checksum(f"{company_prefix}{shipper_ref}")

        return f"(401){company_prefix}{shipper_ref}{check_digit}"
