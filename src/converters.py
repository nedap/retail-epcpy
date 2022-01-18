from schemes.cpi import (
    binary_to_value_cpi96,
    binary_to_value_cpivar,
    tag_to_value_cpi96,
    tag_to_value_cpivar,
)
from schemes.gdti import (
    binary_to_value_gdti96,
    binary_to_value_gdti174,
    tag_to_value_gdti96,
    tag_to_value_gdti174,
)
from schemes.giai import (
    binary_to_value_giai96,
    binary_to_value_giai202,
    tag_to_value_giai96,
    tag_to_value_giai202,
)
from schemes.grai import (
    binary_to_value_grai96,
    binary_to_value_grai170,
    tag_to_value_grai96,
    tag_to_value_grai170,
)
from schemes.gsrn import binary_to_value_gsrn96, tag_to_value_gsrn96
from schemes.gsrnp import binary_to_value_gsrnp96, tag_to_value_gsrnp96
from schemes.itip import (
    binary_to_value_itip110,
    binary_to_value_itip212,
    tag_to_value_itip110,
    tag_to_value_itip212,
)
from schemes.sgcn import binary_to_value_sgcn96, tag_to_value_sgcn96
from schemes.sgln import (
    binary_to_value_sgln96,
    binary_to_value_sgln195,
    tag_to_value_sgln96,
    tag_to_value_sgln195,
)
from schemes.sgtin import (
    binary_to_value_sgtin96,
    binary_to_value_sgtin198,
    tag_to_value_sgtin96,
    tag_to_value_sgtin198,
)
from schemes.sscc import binary_to_value_sscc96, tag_to_value_sscc96

BINARY_CONVERTERS = {
    "sgtin-96": binary_to_value_sgtin96,
    "sgtin-198": binary_to_value_sgtin198,
    "sscc-96": binary_to_value_sscc96,
    "sgln-96": binary_to_value_sgln96,
    "sgln-195": binary_to_value_sgln195,
    "grai-96": binary_to_value_grai96,
    "grai-170": binary_to_value_grai170,
    "giai-96": binary_to_value_giai96,
    "giai-202": binary_to_value_giai202,
    "gsrn-96": binary_to_value_gsrn96,
    "gsrnp-96": binary_to_value_gsrnp96,
    "gdti-96": binary_to_value_gdti96,
    "gdti-174": binary_to_value_gdti174,
    "cpi-96": binary_to_value_cpi96,
    "cpi-var": binary_to_value_cpivar,
    "sgcn-96": binary_to_value_sgcn96,
    "itip-110": binary_to_value_itip110,
    "itip-212": binary_to_value_itip212,
}

TAG_CONVERTERS = {
    "sgtin-96": tag_to_value_sgtin96,
    "sgtin-198": tag_to_value_sgtin198,
    "sscc-96": tag_to_value_sscc96,
    "sgln-96": tag_to_value_sgln96,
    "sgln-195": tag_to_value_sgln195,
    "grai-96": tag_to_value_grai96,
    "grai-170": tag_to_value_grai170,
    "giai-96": tag_to_value_giai96,
    "giai-202": tag_to_value_giai202,
    "gsrn-96": tag_to_value_gsrn96,
    "gsrnp-96": tag_to_value_gsrnp96,
    "gdti-96": tag_to_value_gdti96,
    "gdti-174": tag_to_value_gdti174,
    "cpi-96": tag_to_value_cpi96,
    "cpi-var": tag_to_value_cpivar,
    "sgcn-96": tag_to_value_sgcn96,
    "itip-110": tag_to_value_itip110,
    "itip-212": tag_to_value_itip212,
}
