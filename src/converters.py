from schemes.adi import ADI, binary_to_value_adivar, tag_to_value_adivar
from schemes.bic import BIC
from schemes.cpi import (
    CPI,
    binary_to_value_cpi96,
    binary_to_value_cpivar,
    tag_to_value_cpi96,
    tag_to_value_cpivar,
)
from schemes.gdti import (
    GDTI,
    binary_to_value_gdti96,
    binary_to_value_gdti174,
    tag_to_value_gdti96,
    tag_to_value_gdti174,
)
from schemes.giai import (
    GIAI,
    binary_to_value_giai96,
    binary_to_value_giai202,
    tag_to_value_giai96,
    tag_to_value_giai202,
)
from schemes.gid import GID, binary_to_value_gid96, tag_to_value_gid96
from schemes.ginc import GINC
from schemes.grai import (
    GRAI,
    binary_to_value_grai96,
    binary_to_value_grai170,
    tag_to_value_grai96,
    tag_to_value_grai170,
)
from schemes.gsin import GSIN
from schemes.gsrn import GSRN, binary_to_value_gsrn96, tag_to_value_gsrn96
from schemes.gsrnp import GSRNP, binary_to_value_gsrnp96, tag_to_value_gsrnp96
from schemes.imovn import IMOVN
from schemes.itip import (
    ITIP,
    binary_to_value_itip110,
    binary_to_value_itip212,
    tag_to_value_itip110,
    tag_to_value_itip212,
)
from schemes.pgln import PGLN
from schemes.sgcn import SGCN, binary_to_value_sgcn96, tag_to_value_sgcn96
from schemes.sgln import (
    SGLN,
    binary_to_value_sgln96,
    binary_to_value_sgln195,
    tag_to_value_sgln96,
    tag_to_value_sgln195,
)
from schemes.sgtin import (
    SGTIN,
    binary_to_value_sgtin96,
    binary_to_value_sgtin198,
    tag_to_value_sgtin96,
    tag_to_value_sgtin198,
)
from schemes.sscc import SSCC, binary_to_value_sscc96, tag_to_value_sscc96
from schemes.upui import UPUI
from schemes.usdod import USDOD, binary_to_value_usdod96, tag_to_value_usdod96

BINARY_CONVERTERS = {
    "adi-var": binary_to_value_adivar,
    "cpi-96": binary_to_value_cpi96,
    "cpi-var": binary_to_value_cpivar,
    "gdti-96": binary_to_value_gdti96,
    "gdti-174": binary_to_value_gdti174,
    "giai-96": binary_to_value_giai96,
    "giai-202": binary_to_value_giai202,
    "gid-96": binary_to_value_gid96,
    "grai-96": binary_to_value_grai96,
    "grai-170": binary_to_value_grai170,
    "gsrn-96": binary_to_value_gsrn96,
    "gsrnp-96": binary_to_value_gsrnp96,
    "itip-110": binary_to_value_itip110,
    "itip-212": binary_to_value_itip212,
    "sgcn-96": binary_to_value_sgcn96,
    "sgln-96": binary_to_value_sgln96,
    "sgln-195": binary_to_value_sgln195,
    "sgtin-96": binary_to_value_sgtin96,
    "sgtin-198": binary_to_value_sgtin198,
    "sscc-96": binary_to_value_sscc96,
    "usdod-96": binary_to_value_usdod96,
}

TAG_CONVERTERS = {
    "adi-var": tag_to_value_adivar,
    "cpi-96": tag_to_value_cpi96,
    "cpi-var": tag_to_value_cpivar,
    "gdti-96": tag_to_value_gdti96,
    "gdti-174": tag_to_value_gdti174,
    "giai-96": tag_to_value_giai96,
    "giai-202": tag_to_value_giai202,
    "gid-96": tag_to_value_gid96,
    "grai-96": tag_to_value_grai96,
    "grai-170": tag_to_value_grai170,
    "gsrn-96": tag_to_value_gsrn96,
    "gsrnp-96": tag_to_value_gsrnp96,
    "itip-110": tag_to_value_itip110,
    "itip-212": tag_to_value_itip212,
    "sgcn-96": tag_to_value_sgcn96,
    "sgln-96": tag_to_value_sgln96,
    "sgln-195": tag_to_value_sgln195,
    "sgtin-96": tag_to_value_sgtin96,
    "sgtin-198": tag_to_value_sgtin198,
    "sscc-96": tag_to_value_sscc96,
    "usdod-96": tag_to_value_usdod96,
}

URI_TO_SCHEME = {
    "adi": ADI,
    "bic": BIC,
    "cpi": CPI,
    "gdti": GDTI,
    "giai": GIAI,
    "gid": GID,
    "ginc": GINC,
    "grai": GRAI,
    "gsin": GSIN,
    "gsrn": GSRN,
    "gsrnp": GSRNP,
    "imovn": IMOVN,
    "itip": ITIP,
    "pgln": PGLN,
    "sgcn": SGCN,
    "sgln": SGLN,
    "sgtin": SGTIN,
    "sscc": SSCC,
    "upui": UPUI,
    "usdod": USDOD,
}
