import re

from base_scheme import EPCSchemeNoTagURI
from common import ConvertException
from regex import IMOVN_URI

IMOVN_URI_REGEX = re.compile(IMOVN_URI)


class IMOVN(EPCSchemeNoTagURI):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not IMOVN_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid IMOVN URI {epc_uri}")

        self.epc_uri = epc_uri

        self._vessel_number = epc_uri.split(":")[4]
