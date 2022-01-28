import re

from epcpy.epc_schemes.base_scheme import EPCScheme
from epcpy.utils.common import ConvertException
from epcpy.utils.regex import IMOVN_URI

IMOVN_URI_REGEX = re.compile(IMOVN_URI)


class IMOVN(EPCScheme):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not IMOVN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid IMOVN URI {epc_uri}")

        self.epc_uri = epc_uri

        self._vessel_number = epc_uri.split(":")[4]