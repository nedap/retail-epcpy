import re

from base_scheme import EPCSchemeNoTagURI
from common import ConvertException
from regex import BIC_URI

BIC_URI_REGEX = re.compile(BIC_URI)


class BIC(EPCSchemeNoTagURI):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not BIC_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid BIC URI {epc_uri}")

        self.epc_uri = epc_uri

        container_code = epc_uri.split(":")[4]
        self.owner_code = container_code[0:3]
        self.equipment_category_identifier = container_code[3]
        self.serial = container_code[4:10]
        self.check_digit = container_code[10]
        self.container_code = container_code
