import re

from epcpy.epc_schemes.base_scheme import EPCScheme
from epcpy.utils.common import ConvertException
from epcpy.utils.regex import BIC_URI

BIC_URI_REGEX = re.compile(BIC_URI)


class BIC(EPCScheme):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not BIC_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid BIC URI {epc_uri}")

        self.epc_uri = epc_uri

        container_code = epc_uri.split(":")[4]
        self._container_code = container_code

        self._owner_code = container_code[0:3]
        self._equipment_category_identifier = container_code[3]
        self._serial = container_code[4:10]
        self._check_digit = container_code[10]
