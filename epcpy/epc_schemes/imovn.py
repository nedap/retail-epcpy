import re

from epcpy.epc_schemes.base_scheme import EPCScheme
from epcpy.utils.common import ConvertException
from epcpy.utils.regex import IMOVN_URI

IMOVN_URI_REGEX = re.compile(IMOVN_URI)


class IMOVN(EPCScheme):
    """IMOVN EPC scheme implementation.

    IMOVN pure identities are of the form:
        urn:epc:id:imovn:<IMOvesselNumber>

    Example:
        urn:epc:id:imovn:9176187

    This class can be created using EPC pure identities via its constructor
    """

    def __init__(self, epc_uri) -> None:
        super().__init__(epc_uri)

        if not IMOVN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid IMOVN URI {epc_uri}")

        self.epc_uri = epc_uri

        self._vessel_number = epc_uri.split(":")[4]
