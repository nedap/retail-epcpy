# Generic
CPREF_COMPONENT = "([0-9A-Z-]|%2F|%23)+"
NUMERIC_COMPONENT = "(0|[1-9]\d*)"
GS3A3_CHAR = "((%[0-9a-fA-F])|([a-zA-Z0-9!'()*+,-.:;=_]))"
GS3A3_COMPONENT = f"{GS3A3_CHAR}+"
PADDED_NUMERIC_COMPONENT = "\d+"
PADDED_NUMERIC_COMPONENT_OR_EMPTY = "\d*"
VERIFY_GS3A3_CHARS = "[a-zA-Z0-9!'()*+,-.:;=_\"%&/<>?]+"
GS1_ELEM_CHARS = "[a-zA-Z0-9!'()*+,-.:;=_\"%&/<>?]"
GS1_ELEM_CHARS_CPI = "[0-9A-Z\/\-\#]"
DIGIT = "\d"

FOUR_PADDED_NUMERIC_COMPONENTS = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}"

# EPC Pure Identity URIs
SGTIN_URI_BODY = (
    f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}"
)
SGTIN_URI = f"urn:epc:id:sgtin:{SGTIN_URI_BODY}"

SSCC_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}"
SSCC_URI = f"urn:epc:id:sscc:{SSCC_URI_BODY}"

SGLN_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{GS3A3_COMPONENT}"
SGLN_URI = f"urn:epc:id:sgln:{SGLN_URI_BODY}"

GRAI_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{GS3A3_COMPONENT}"
GRAI_URI = f"urn:epc:id:grai:{GRAI_URI_BODY}"

GIAI_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}"
GIAI_URI = f"urn:epc:id:giai:{GIAI_URI_BODY}"

GSRN_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}"
GSRN_URI = f"urn:epc:id:gsrn:{GSRN_URI_BODY}"

GSRNP_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}"
GSRNP_URI = f"urn:epc:id:gsrnp:{GSRN_URI_BODY}"

GDTI_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{GS3A3_COMPONENT}"
GDTI_URI = f"urn:epc:id:gdti:{GDTI_URI_BODY}"

CPI_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{CPREF_COMPONENT}\.{NUMERIC_COMPONENT}"
CPI_URI = f"urn:epc:id:cpi:{CPI_URI_BODY}"

SGCN_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{PADDED_NUMERIC_COMPONENT}"
SGCN_URI = f"urn:epc:id:sgcn:{SGCN_URI_BODY}"

GINC_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}"
GINC_URI = f"urn:epc:id:ginc:{GINC_URI_BODY}"

GSIN_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}"
GSIN_URI = f"urn:epc:id:gsin:{GSIN_URI_BODY}"

ITIP_URI_BODY = f"{FOUR_PADDED_NUMERIC_COMPONENTS}\.{GS3A3_COMPONENT}"
ITIP_URI = f"urn:epc:id:itip:{ITIP_URI_BODY}"

UPUI_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{GS3A3_COMPONENT}"
UPUI_URI = f"urn:epc:id:upui:{UPUI_URI_BODY}"

PGLN_URI_BODY = f"{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}"
PGLN_URI = f"urn:epc:id:pgln:{PGLN_URI_BODY}"

GID_URI_BODY = f"{NUMERIC_COMPONENT}\.{NUMERIC_COMPONENT}\.{NUMERIC_COMPONENT}"
GID_URI = f"urn:epc:id:gid:{GID_URI_BODY}"

CAGE_CODE_OR_DODAAC = "([0-9A-HJ-NP-Z]){5,6}"
USDOD_URI_BODY = f"{CAGE_CODE_OR_DODAAC}\.{NUMERIC_COMPONENT}"
USDOD_URI = f"urn:epc:id:usdod:{USDOD_URI_BODY}"

ADI_CHAR = "([A-Z0-9-]|(%2F))"
ADI_URI_BODY = f"{CAGE_CODE_OR_DODAAC}\.{ADI_CHAR}*\.(%23)?{ADI_CHAR}+"
ADI_URI = f"urn:epc:id:adi:{ADI_URI_BODY}"

BIC_URI_BODY = "[A-HJ-NP-Z]{3}[JUZ][0-9]{7}"
BIC_URI = f"urn:epc:id:bic:{BIC_URI_BODY}"

IMOVN_URI_BODY = "[0-9]{7}"
IMOVN_URI = f"urn:epc:id:imovn:{IMOVN_URI_BODY}"

EPC_URI = (
    f"{SGTIN_URI}|{SSCC_URI}|{SGLN_URI}|{GRAI_URI}|{GIAI_URI}|{GSRN_URI}|{GSRNP_URI}|{GDTI_URI}"
    f"|{CPI_URI}|{SGCN_URI}|{GINC_URI}|{GSIN_URI}|{ITIP_URI}|{UPUI_URI}|{PGLN_URI}|{GID_URI}"
    f"|{USDOD_URI}|{ADI_URI}|{BIC_URI}|{IMOVN_URI}"
)

# EPC IDPAT URIs
SGTIN_IDPAT_URI_BODY = f"sgtin:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
SSCC_IDPAT_URI_BODY = f"sscc:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
SGLN_GRAI_IDPAT_URI_BODY_MAIN = f"({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{GS3A3_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
SGLN_IDPAT_URI_BODY = f"sgln:{SGLN_GRAI_IDPAT_URI_BODY_MAIN}"
GRAI_IDPAT_URI_BODY = f"grai:{SGLN_GRAI_IDPAT_URI_BODY_MAIN}"
GIAI_IDPAT_URI_BODY = f"giai:({PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
GSRN_IDPAT_URI_BODY = f"gsrn:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
GSRNP_IDPAT_URI_BODY = f"gsrnp:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
GDTI_IDPAT_URI_BODY = f"gdti:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{GS3A3_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
CPI_IDPAT_URI_BODY = f"cpi:({PADDED_NUMERIC_COMPONENT}\.{CPREF_COMPONENT}\.{NUMERIC_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.{CPREF_COMPONENT}\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
SGCN_IDPAT_URI_BODY = f"sgcn:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.{PADDED_NUMERIC_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
GINC_IDPAT_URI_BODY = f"ginc:({PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
GSIN_IDPAT_URI_BODY = f"gsin:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
ITIP_IDPAT_URI_BODY = f"itip:({FOUR_PADDED_NUMERIC_COMPONENTS}\.{GS3A3_COMPONENT}|{FOUR_PADDED_NUMERIC_COMPONENTS}\.\*|{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.\*\.\*\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*\.\*\.\*|\*\.\*\*\.\*\.\*)"
UPUI_IDPAT_URI_BODY = f"upui:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.{GS3A3_COMPONENT}|{PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT}\.\*|{PADDED_NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
PGLN_IDPAT_URI_BODY = f"pgln:({PADDED_NUMERIC_COMPONENT}\.{PADDED_NUMERIC_COMPONENT_OR_EMPTY}|{PADDED_NUMERIC_COMPONENT}\.\*|\*\.\*)"
GID_IDPAT_URI_BODY = f"gid:({NUMERIC_COMPONENT}\.{NUMERIC_COMPONENT}\.{NUMERIC_COMPONENT}|{NUMERIC_COMPONENT}\.{NUMERIC_COMPONENT}\.\*|{NUMERIC_COMPONENT}\.\*\.\*|\*\.\*\.\*)"
USDOD_IDPAT_URI_BODY = f"usdod:({CAGE_CODE_OR_DODAAC}\.{NUMERIC_COMPONENT}|{CAGE_CODE_OR_DODAAC}\.\*|\*\.\*)"
ADI_IDPAT_URI_BODY = f"adi:({CAGE_CODE_OR_DODAAC}\.{ADI_CHAR}*\.(%23)?{ADI_CHAR}+|{CAGE_CODE_OR_DODAAC}\.{ADI_CHAR}*\.\*|{CAGE_CODE_OR_DODAAC}\.\*\.\*|\*\.\*\.\*)"

IDPAT_BODY = (
    f"({SGTIN_IDPAT_URI_BODY}|{SSCC_IDPAT_URI_BODY}|{SGLN_IDPAT_URI_BODY}|{GRAI_IDPAT_URI_BODY}"
    f"|{GIAI_IDPAT_URI_BODY}|{GSRN_IDPAT_URI_BODY}|{GSRNP_IDPAT_URI_BODY}|{GDTI_IDPAT_URI_BODY}"
    f"|{CPI_IDPAT_URI_BODY}|{SGCN_IDPAT_URI_BODY}|{GINC_IDPAT_URI_BODY}|{GSIN_IDPAT_URI_BODY}"
    f"|{ITIP_IDPAT_URI_BODY}|{UPUI_IDPAT_URI_BODY}|{PGLN_IDPAT_URI_BODY}|{GID_IDPAT_URI_BODY}"
    f"|{USDOD_IDPAT_URI_BODY}|{ADI_IDPAT_URI_BODY})"
)
IDPAT_URI = f"urn:epc:idpat:{IDPAT_BODY}"

# EPC Tag URIs
SGTIN_TAG_URI_BODY = f"(sgtin-96|sgtin-198):{NUMERIC_COMPONENT}\.{SGTIN_URI_BODY}"
SSCC_TAG_URI_BODY = f"sscc-96:{NUMERIC_COMPONENT}\.{SSCC_URI_BODY}"
SGLN_TAG_URI_BODY = f"(sgln-96|sgln-195):{NUMERIC_COMPONENT}\.{SGLN_URI_BODY}"
GRAI_TAG_URI_BODY = f"(grai-96|grai-170):{NUMERIC_COMPONENT}\.{GRAI_URI_BODY}"
GIAI_TAG_URI_BODY = f"(giai-96|giai-202):{NUMERIC_COMPONENT}\.{GIAI_URI_BODY}"
GSRN_TAG_URI_BODY = f"gsrn-96:{NUMERIC_COMPONENT}\.{GSRN_URI_BODY}"
GSRNP_TAG_URI_BODY = f"gsrnp-96:{NUMERIC_COMPONENT}\.{GSRNP_URI_BODY}"
GDTI_TAG_URI_BODY = f"(gdti-96|gdti-174):{NUMERIC_COMPONENT}\.{GDTI_URI_BODY}"
CPI_TAG_URI_BODY = f"(cpi-96|cpi-var):{NUMERIC_COMPONENT}\.{CPI_URI_BODY}"
SGCN_TAG_URI_BODY = f"sgcn-96:{NUMERIC_COMPONENT}\.{SGCN_URI_BODY}"
ITIP_TAG_URI_BODY = f"(itip-110|itip-212):{NUMERIC_COMPONENT}\.{ITIP_URI_BODY}"
GID_TAG_URI_BODY = f"gid-96:{GID_URI_BODY}"
USDOD_TAG_URI_BODY = f"usdod-96:{NUMERIC_COMPONENT}\.{USDOD_URI_BODY}"
ADI_TAG_URI_BODY = f"adi-var:{NUMERIC_COMPONENT}\.{ADI_URI_BODY}"

TAG_URI_BODY = (
    f"({SGTIN_TAG_URI_BODY}|{SSCC_TAG_URI_BODY}|{SGLN_TAG_URI_BODY}|{GRAI_TAG_URI_BODY}"
    f"|{GIAI_TAG_URI_BODY}|{GSRN_TAG_URI_BODY}|{GSRNP_TAG_URI_BODY}|{GDTI_TAG_URI_BODY}"
    f"|{CPI_TAG_URI_BODY}|{SGCN_TAG_URI_BODY}|{ITIP_TAG_URI_BODY}|{GID_TAG_URI_BODY}"
    f"|{USDOD_TAG_URI_BODY}|{ADI_TAG_URI_BODY})"
)
TAG_URI = f"urn:epc:tag:{TAG_URI_BODY}"

# GS1 element strings
SGTIN_GS1_ELEMENT_STRING = f"\(01\){DIGIT}{{14}}\(21\){GS1_ELEM_CHARS}{{1,20}}"
SSCC_GS1_ELEMENT_STRING = f"\(00\){DIGIT}{{18}}"
SGLN_GS1_ELEMENT_STRING = f"\(414\){DIGIT}{{13}}\(254\){GS1_ELEM_CHARS}{{1,20}}"
GRAI_GS1_ELEMENT_STRING = f"\(8003\)0{DIGIT}{{13}}{GS1_ELEM_CHARS}{{1,16}}"
GIAI_GS1_ELEMENT_STRING = f"\(8004\){DIGIT}{{6,12}}{GS1_ELEM_CHARS}{{1,24}}"
GSRN_GS1_ELEMENT_STRING = f"\(8018\){DIGIT}{{18}}"
GSRNP_GS1_ELEMENT_STRING = f"\(8017\){DIGIT}{{18}}"
GDTI_GS1_ELEMENT_STRING = f"\(253\){DIGIT}{{13}}{GS1_ELEM_CHARS}{{1,17}}"
CPI_GS1_ELEMENT_STRING = (
    f"\(8010\){DIGIT}{{6,12}}{GS1_ELEM_CHARS_CPI}{{,24}}\(8011\){DIGIT}{{1,12}}"
)
SGCN_GS1_ELEMENT_STRING = f"\(255\){DIGIT}{{13}}{GS1_ELEM_CHARS}{{1,12}}"
GINC_GS1_ELEMENT_STRING = f"\(401\){DIGIT}{{6,12}}{GS1_ELEM_CHARS}{{1,24}}"
GSIN_GS1_ELEMENT_STRING = f"\(402\){DIGIT}{{17}}"
ITIP_GS1_ELEMENT_STRING = f"\(8006\){DIGIT}{{18}}\(21\){GS1_ELEM_CHARS}{{1,20}}"
UPUI_GS1_ELEMENT_STRING = f"\(01\){DIGIT}{{14}}\(235\){GS1_ELEM_CHARS}{{1,28}}"

GS1_ELEMENT_STRING = (
    f"({SGTIN_GS1_ELEMENT_STRING}|{SSCC_GS1_ELEMENT_STRING}|{SGLN_GS1_ELEMENT_STRING}"
    f"|{GRAI_GS1_ELEMENT_STRING}|{GIAI_GS1_ELEMENT_STRING}|{GSRN_GS1_ELEMENT_STRING}"
    f"|{GSRNP_GS1_ELEMENT_STRING}|{GDTI_GS1_ELEMENT_STRING}|{CPI_GS1_ELEMENT_STRING}"
    f"|{SGCN_GS1_ELEMENT_STRING}|{GINC_GS1_ELEMENT_STRING}|{GSIN_GS1_ELEMENT_STRING}"
    f"|{ITIP_GS1_ELEMENT_STRING}|{UPUI_GS1_ELEMENT_STRING})"
)
