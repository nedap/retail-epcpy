from epcpy.epc_schemes import (
    ADI,
    BIC,
    CPI,
    GDTI,
    GIAI,
    GID,
    GINC,
    GRAI,
    GSIN,
    GSRN,
    GSRNP,
    IMOVN,
    ITIP,
    PGLN,
    SGCN,
    SGLN,
    SGTIN,
    SSCC,
    UPUI,
    USDOD,
)
from epcpy.epc_schemes.sgtin import GTIN_TYPE

VALID_TEST_DATA = [
    {
        "scheme": ADI,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.2WMA-52",
        "tag_uri": "urn:epc:tag:adi-var:5.W81X9C.3KL984PX1.2WMA-52",
        "hex": "3B157E316390F32CCE78D106310325CD06DD7200",
        "binary": "0011101100010101011111100011000101100011100100001111001100101100110011100111100011010001000001100011000100000011001001011100110100000110110111010111001000000000",
    },
    {
        "scheme": BIC,
        "tag_encodable": False,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:bic:CSQJ3054381",
    },
    {
        "scheme": CPI,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": True,
        "uri": "urn:epc:id:cpi:0614141.12-456.123456789",
        "gs1_element_string": "(8010)061414112-456(8011)123456789",
        "tag_uri": "urn:epc:tag:cpi-var:0.0614141.12-456.123456789",
        "hex": "3D14257BF71CADD35D8000075BCD1500",
        "binary": "00111101000101000010010101111011111101110001110010101101110100110101110110000000000000000000011101011011110011010001010100000000",
    },
    {
        "scheme": GDTI,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gdti:0614141.12345.ABCD1234%2F",
        "gs1_key": "0614141123452ABCD1234/",
        "gs1_element_string": "(253)0614141123452ABCD1234/",
        "company_prefix_length": 7,
        "tag_uri": "urn:epc:tag:gdti-174:0.0614141.12345.ABCD1234%2F",
        "hex": "3E14257BF460730614388C593368BC00000000000000",
        "binary": "00111110000101000010010101111011111101000110000001110011000001100001010000111000100011000101100100110011011010001011110000000000000000000000000000000000000000000000000000000000",
    },
    {
        "scheme": GIAI,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:giai:0614141.1ABc%2FD",
        "gs1_key": "06141411ABc/D",
        "gs1_element_string": "(8004)06141411ABc/D",
        "company_prefix_length": 7,
        "tag_uri": "urn:epc:tag:giai-202:0.0614141.1ABc%2FD",
        "hex": "3814257BF58C1858D7C400000000000000000000000000000000",
        "binary": "0011100000010100001001010111101111110101100011000001100001011000110101111100010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    {
        "scheme": GID,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:gid:268435455.16777215.68719476735",
        "tag_uri": "urn:epc:tag:gid-96:268435455.16777215.68719476735",
        "hex": "35FFFFFFFFFFFFFFFFFFFFFF",
        "binary": "001101011111111111111111111111111111111111111111111111111111111111111111111111111111111111111111",
    },
    {
        "scheme": GINC,
        "tag_encodable": False,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:ginc:061411.01ABc%2FD",
        "gs1_key": "06141101ABc/D",
        "gs1_element_string": "(401)06141101ABc/D",
        "company_prefix_length": 6,
    },
    {
        "scheme": GRAI,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%2F",
        "gs1_key": "0614141123452ABCD1234/",
        "gs1_element_string": "(8003)00614141123452ABCD1234/",
        "company_prefix_length": 7,
        "tag_uri": "urn:epc:tag:grai-170:0.0614141.12345.ABCD1234%2F",
        "hex": "3714257BF40C0E60C287118B266D1780000000000000",
        "binary": "00110111000101000010010101111011111101000000110000001110011000001100001010000111000100011000101100100110011011010001011110000000000000000000000000000000000000000000000000000000",
    },
    {
        "scheme": GSIN,
        "tag_encodable": False,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gsin:061414.0123456789",
        "gs1_key": "06141401234567891",
        "gs1_element_string": "(402)06141401234567891",
        "company_prefix_length": 6,
    },
    {
        "scheme": GSRN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gsrn:012345678901.01234",
        "gs1_key": "012345678901012342",
        "gs1_element_string": "(8018)012345678901012342",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:gsrn-96:0.012345678901.01234",
        "hex": "2D000B7F7070D404D2000000",
        "binary": "001011010000000000001011011111110111000001110000110101000000010011010010000000000000000000000000",
    },
    {
        "scheme": GSRNP,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gsrnp:012345678901.01234",
        "gs1_key": "012345678901012342",
        "gs1_element_string": "(8017)012345678901012342",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:gsrnp-96:0.012345678901.01234",
        "hex": "2E000B7F7070D404D2000000",
        "binary": "001011100000000000001011011111110111000001110000110101000000010011010010000000000000000000000000",
    },
    {
        "scheme": IMOVN,
        "tag_encodable": False,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:imovn:9176187",
    },
    {
        "scheme": ITIP,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": True,
        "uri": "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
        "gs1_element_string": "(8006)001234567890120000(21)ABCDEFGHIJKLMNOP/RST",
        "tag_uri": "urn:epc:tag:itip-212:0.012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
        "hex": "41000B7F7070D40000830A1C48B1A3C8932A5CC9B3A7D05F4A9D4000",
        "binary": "01000001000000000000101101111111011100000111000011010100000000000000000010000011000010100001110001001000101100011010001111001000100100110010101001011100110010011011001110100111110100000101111101001010100111010100000000000000",
    },
    {
        "scheme": PGLN,
        "tag_encodable": False,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:pgln:0123456789.01",
        "gs1_key": "0123456789012",
        "gs1_element_string": "(417)0123456789012",
        "company_prefix_length": 10,
    },
    {
        "scheme": SGCN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgcn:401234512345..1",
        "gs1_key": "40123451234561",
        "gs1_element_string": "(255)40123451234561",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:sgcn-96:7.401234512345..1",
        "hex": "3FE175ADC32764000000000B",
        "binary": "001111111110000101110101101011011100001100100111011001000000000000000000000000000000000000001011",
    },
    {
        "scheme": SGLN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQR",
        "gs1_key": "0614111234560",
        "gs1_element_string": "(414)0614111234560(254)A/-BCDEFGHIJKLMNOPQR",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:sgln-195:0.061411123456..A%2F-BCDEFGHIJKLMNOPQR",
        "hex": "390039318D8401057AD850E2458D1E449952E64D9D3E851A4000",
        "binary": "0011100100000000001110010011000110001101100001000000000100000101011110101101100001010000111000100100010110001101000111100100010010011001010100101110011001001101100111010011111010000101000110100100000000000000",
    },
    {
        "scheme": SGTIN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
        "gs1_key": "00000095010939",
        "gs1_element_string": "(01)00000095010939(21)Serial",
        "company_prefix_length": 8,
        "tag_uri": "urn:epc:tag:sgtin-198:2.00000950.01093.Serial",
        "hex": "36500001DB011169E5E5A70EC000000000000000000000000000",
        "binary": "0011011001010000000000000000000111011011000000010001000101101001111001011110010110100111000011101100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
    },
    {
        "scheme": SGTIN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
        "gs1_key": "0000095010939",
        "gs1_element_string": "(01)00000095010939(21)Serial",
        "company_prefix_length": 8,
        "tag_uri": "urn:epc:tag:sgtin-198:2.00000950.01093.Serial",
        "hex": "36500001DB011169E5E5A70EC000000000000000000000000000",
        "binary": "0011011001010000000000000000000111011011000000010001000101101001111001011110010110100111000011101100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
    },
    {
        "scheme": SGTIN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
        "gs1_key": "95010939",
        "gs1_element_string": "(01)00000095010939(21)Serial",
        "company_prefix_length": 8,
        "tag_uri": "urn:epc:tag:sgtin-198:2.00000950.01093.Serial",
        "hex": "36500001DB011169E5E5A70EC000000000000000000000000000",
        "binary": "0011011001010000000000000000000111011011000000010001000101101001111001011110010110100111000011101100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
    },
    {
        "scheme": SSCC,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sscc:061414123456.12345",
        "gs1_key": "106141412345623458",
        "gs1_element_string": "(00)106141412345623458",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:sscc-96:0.061414123456.12345",
        "hex": "31003932449F003039000000",
        "binary": "001100010000000000111001001100100100010010011111000000000011000000111001000000000000000000000000",
    },
    {
        "scheme": UPUI,
        "tag_encodable": False,
        "gs1_keyed": False,
        "gs1_element": True,
        "uri": "urn:epc:id:upui:1234567.089456.51qIgY)%3C%26Jp3*j7'SDB",
        "gs1_element_string": "(01)01234567894560(235)51qIgY)<&Jp3*j7'SDB",
    },
    {
        "scheme": USDOD,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:usdod:2S194.68719476735",
        "tag_uri": "urn:epc:tag:usdod-96:15.2S194.68719476735",
        "hex": "2FF203253313934FFFFFFFFF",
        "binary": "001011111111001000000011001001010011001100010011100100110100111111111111111111111111111111111111",
    },
]

VALID_ID_PATTERNS = [
    {
        "scheme": GDTI,
        "idpat": "urn:epc:idpat:gdti:0614141.12345.*",
        "gs1_key": "0614141123452*",
    },
    {
        "scheme": GIAI,
        "idpat": "urn:epc:idpat:giai:0614141.*",
        "gs1_key": "0614141*",
    },
    {
        "scheme": GINC,
        "idpat": "urn:epc:idpat:ginc:061411.*",
        "gs1_key": "061411*",
    },
    {
        "scheme": GRAI,
        "idpat": "urn:epc:idpat:grai:0614141.12345.*",
        "gs1_key": "0614141123452*",
    },
    {
        "scheme": GSIN,
        "idpat": "urn:epc:idpat:gsin:061414.0123456789",
        "gs1_key": "06141401234567891",
    },
    {
        "scheme": GSRN,
        "idpat": "urn:epc:idpat:gsrn:012345678901.01234",
        "gs1_key": "012345678901012342",
    },
    {
        "scheme": GSRNP,
        "idpat": "urn:epc:idpat:gsrnp:012345678901.01234",
        "gs1_key": "012345678901012342",
    },
    {
        "scheme": PGLN,
        "idpat": "urn:epc:idpat:pgln:0123456789.01",
        "gs1_key": "0123456789012",
    },
    {
        "scheme": SGCN,
        "idpat": "urn:epc:idpat:sgcn:401234512345..1",
        "gs1_key": "40123451234561",
    },
    {
        "scheme": SGLN,
        "idpat": "urn:epc:idpat:sgln:061411123456..*",
        "gs1_key": "0614111234560",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.01093.*",
        "gs1_key": "00000095010939",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.01093.*",
        "gs1_key": "0000095010939",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.01093.*",
        "gs1_key": "95010939",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
    },
    {
        "scheme": SSCC,
        "idpat": "urn:epc:idpat:sscc:061414123456.12345",
        "gs1_key": "106141412345623458",
    },
]


INVALID_ID_PATTERNS = [
    {
        "scheme": GDTI,
        "idpat": "urn:epc:idpat:gdti:0614141.*.*",
    },
    {
        "scheme": GIAI,
        "idpat": "urn:epc:idpat:giai:*.*",
    },
    {
        "scheme": GINC,
        "idpat": "urn:epc:idpat:ginc:*.*",
        "gs1_key": "061411*",
    },
    {
        "scheme": GRAI,
        "idpat": "urn:epc:idpat:grai:0614141.*.*",
    },
    {
        "scheme": GSIN,
        "idpat": "urn:epc:idpat:gsin:061414.*",
    },
    {
        "scheme": GSRN,
        "idpat": "urn:epc:idpat:gsrn:012345678901.*",
    },
    {
        "scheme": GSRNP,
        "idpat": "urn:epc:idpat:gsrnp:012345678901.*",
    },
    {
        "scheme": PGLN,
        "idpat": "urn:epc:idpat:pgln:0123456789.*",
    },
    {
        "scheme": SGCN,
        "idpat": "urn:epc:idpat:sgcn:401234512345..*",
    },
    {
        "scheme": SGLN,
        "idpat": "urn:epc:idpat:sgln:061411123456.*.*",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.*.*",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.*.*",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.*.*",
    },
    {
        "scheme": SSCC,
        "idpat": "urn:epc:idpat:sscc:061414123456.*",
    },
]