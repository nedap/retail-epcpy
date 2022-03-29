def convert_digital_link_escaped_characters(digital_link: str) -> str:
    return (
        digital_link.replace("%20", " ")
        .replace("%21", "!")
        .replace("%23", "#")
        .replace("%25", "%")
        .replace("%26", "&")
        .replace("%28", "(")
        .replace("%29", ")")
        .replace("%2A", "*")
        .replace("%2B", "+")
        .replace("%2C", ",")
        .replace("%2F", "/")
        .replace("%3A", ":")
    )


CHECK_DIGIT_POSITIONS = {
    "GTIN": -1,
    "ITIP": 14,
    "SSCC": 18,
    "GDTI": 13,
    "GLN": 13,
    "GRAI": 13,
    "GSRN": 18,
    "GRSNP": 18,
    "GSIN": 17,
    "GCN": 13,
    "02": -1,
    "410": 13,
    "411": 13,
    "412": 13,
    "413": 13,
    "414": 13,
    "415": 13,
    "416": 13,
}


def validate(digital_link):
    digital_link = convert_digital_link_escaped_characters(digital_link)

    # Validate length

    # Validate character set

    # Validate check digit (if available)
    pass
