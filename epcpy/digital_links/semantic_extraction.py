import calendar
from datetime import datetime

from epcpy.digital_links.model import BLANK_NODE, RDF, DigitalLink

STRING_SEMANTICS = {
    "01": ["gs1:gtin", "schema:gtin"],
    "10": ["gs1:batchLot"],
    "21": ["gs1:serialNumber"],
    "22": ["gs1:cpv"],
    "235": ["gs1:tpx"],
}
DATE_SEMANTICS = {
    "11": "gs1:productionDate",
    "12": "gs1:dueDate",
    "13": "gs1:packagingDate",
    "15": "gs1:bestBeforeDate",
    "16": "gs1:sellByDate",
    "17": "gs1:expirationDate",
    "7006": "gs1:firstFreezeDate",
    "exp": "gs1:expirationDate",
}
DATETIME_MIN_SEMANTICS = {
    "7003": "gs1:expirationDateTime",
    "expdt": "gs1:expirationDateTime",
}
DATETIME_SEC_SEMANTICS = {"11": "gs1:productionDateTime"}
DATE_RANGE_SEMANTICS = {"7007": "gs1:harvestDate"}
QUANTATIVE_VALUES_SEMANTICS = {
    "310": {
        "properties": ["gs1:netWeight"],
        "rec_20": "KGM",
    },
    "320": {
        "properties": ["gs1:netWeight"],
        "rec_20": "LBR",
    },
    "356": {
        "properties": ["gs1:netWeight"],
        "rec_20": "APZ",
    },
    "357": {
        "properties": ["gs1:netWeight"],
        "rec_20": "ONZ",
    },
    "330": {
        "properties": ["gs1:grossWeight"],
        "rec_20": "KGM",
    },
    "340": {
        "properties": ["gs1:grossWeight"],
        "rec_20": "LBR",
    },
    "315": {
        "properties": ["gs1:netContent"],
        "rec_20": "LTR",
    },
    "316": {
        "properties": ["gs1:netContent"],
        "rec_20": "MTQ",
    },
    "360": {
        "properties": ["gs1:netContent"],
        "rec_20": "QT",
    },
    "361": {
        "properties": ["gs1:netContent"],
        "rec_20": "GLL",
    },
    "365": {
        "properties": ["gs1:netContent"],
        "rec_20": "FTQ",
    },
    "364": {
        "properties": ["gs1:netContent"],
        "rec_20": "INQ",
    },
    "366": {
        "properties": ["gs1:netContent"],
        "rec_20": "YDQ",
    },
    "335": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "LTR",
    },
    "336": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "MTQ",
    },
    "368": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "FTQ",
    },
    "367": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "INQ",
    },
    "369": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "YDQ",
    },
    "363": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "GLL",
    },
    "362": {
        "properties": ["gs1:grossVolume"],
        "rec_20": "QT",
    },
    "328": {
        "properties": ["gs1:outOfPackageDepth"],
        "rec_20": "FOT",
    },
    "327": {
        "properties": ["gs1:outOfPackageDepth"],
        "rec_20": "INH",
    },
    "313": {
        "properties": ["gs1:outOfPackageDepth"],
        "rec_20": "MTR",
    },
    "329": {
        "properties": ["gs1:outOfPackageDepth"],
        "rec_20": "YRD",
    },
    "348": {
        "properties": ["gs1:inPackageDepth"],
        "rec_20": "FOT",
    },
    "347": {
        "properties": ["gs1:inPackageDepth"],
        "rec_20": "INH",
    },
    "333": {
        "properties": ["gs1:inPackageDepth"],
        "rec_20": "MTR",
    },
    "349": {
        "properties": ["gs1:inPackageDepth"],
        "rec_20": "YRD",
    },
    "322": {
        "properties": ["gs1:outOfPackageLength"],
        "rec_20": "FOT",
    },
    "321": {
        "properties": ["gs1:outOfPackageLength"],
        "rec_20": "INH",
    },
    "311": {
        "properties": ["gs1:outOfPackageLength"],
        "rec_20": "MTR",
    },
    "323": {
        "properties": ["gs1:outOfPackageLength"],
        "rec_20": "YRD",
    },
    "342": {
        "properties": ["gs1:inPackageLength"],
        "rec_20": "FOT",
    },
    "341": {
        "properties": ["gs1:inPackageLength"],
        "rec_20": "INH",
    },
    "331": {
        "properties": ["gs1:inPackageLength"],
        "rec_20": "MTR",
    },
    "343": {
        "properties": ["gs1:inPackageLength"],
        "rec_20": "YRD",
    },
    "325": {
        "properties": ["gs1:outOfPackageWidth"],
        "rec_20": "FOT",
    },
    "324": {
        "properties": ["gs1:outOfPackageWidth"],
        "rec_20": "INH",
    },
    "312": {
        "properties": ["gs1:outOfPackageWidth"],
        "rec_20": "MTR",
    },
    "346": {
        "properties": ["gs1:outOfPackageWidth", "gs1:inPackageWidth"],
        "rec_20": "YRD",
    },
    "345": {
        "properties": ["gs1:inPackageWidth"],
        "rec_20": "FOT",
    },
    "344": {
        "properties": ["gs1:inPackageWidth"],
        "rec_20": "INH",
    },
    "332": {
        "properties": ["gs1:inPackageWidth"],
        "rec_20": "MTR",
    },
    "351": {
        "properties": ["gs1:netArea"],
        "rec_20": "FTK",
    },
    "350": {
        "properties": ["gs1:netArea"],
        "rec_20": "INK",
    },
    "314": {
        "properties": ["gs1:netArea"],
        "rec_20": "MTK",
    },
    "352": {
        "properties": ["gs1:netArea"],
        "rec_20": "YDK",
    },
    "354": {
        "properties": ["gs1:grossArea"],
        "rec_20": "FTK",
    },
    "353": {
        "properties": ["gs1:grossArea"],
        "rec_20": "INK",
    },
    "334": {
        "properties": ["gs1:grossArea"],
        "rec_20": "MTK",
    },
    "355": {
        "properties": ["gs1:grossArea"],
        "rec_20": "YDK",
    },
    "337": {
        "properties": ["gs1:massPerUnitArea"],
        "rec_20": "28",
    },
}


def parse_six_digit_date(date: str) -> str:
    if date[-2:] != "00":
        parsed_date = datetime.strptime(date, "%y%m%d")
    else:
        parsed_date = datetime.strptime(date[:4], "%y%m")
        parsed_date = parsed_date.replace(
            day=calendar.monthrange(parsed_date.year, parsed_date.month)[1]
        )

    return parsed_date.strftime("%Y-%m-%d")


def process_string_semantics(
    ai: str, val: str, rdf_subject: str, digital_link: DigitalLink
):
    for property in STRING_SEMANTICS[ai]:
        digital_link.add_rdf(RDF(rdf_subject, property, val))


def process_date_semantics(
    ai: str, val: str, rdf_subject: str, digital_link: DigitalLink
):
    processed_date = parse_six_digit_date(val)
    digital_link.add_rdf(RDF(rdf_subject, DATE_SEMANTICS[ai], processed_date))


def process_datetime_min_semantics(
    ai: str, val: str, rdf_subject: str, digital_link: DigitalLink
):
    processed_date = parse_six_digit_date(val[:6])
    hours = val[6:8]
    minutes = val[8:10]
    processed_datetime = f"{processed_date}T{hours}:{minutes}:00"

    digital_link.add_rdf(
        RDF(rdf_subject, DATETIME_MIN_SEMANTICS[ai], processed_datetime)
    )


def process_datetime_sec_semantics(
    ai: str, val: str, rdf_subject: str, digital_link: DigitalLink
):
    processed_date = parse_six_digit_date(val[:6])
    hours = val[6:8]
    minutes = val[8:10]
    seconds = val[10:12]
    processed_datetime = f"{processed_date}T{hours}:{minutes}:{seconds}"

    digital_link.add_rdf(
        RDF(rdf_subject, DATETIME_SEC_SEMANTICS[ai], processed_datetime)
    )


def process_date_range_semantics(
    ai: str, val: str, rdf_subject: str, digital_link: DigitalLink
):
    predicate = DATE_RANGE_SEMANTICS[ai]
    if len(val) != 12:
        processed_date = parse_six_digit_date(val[:6])
        digital_link.add_rdf(RDF(rdf_subject, predicate, processed_date))
    else:
        processed_date_start = parse_six_digit_date(val[:6])
        processed_date_end = parse_six_digit_date(val[6:12])

        digital_link.add_rdf(
            RDF(rdf_subject, f"{predicate}Start", processed_date_start)
        )
        digital_link.add_rdf(RDF(rdf_subject, f"{predicate}End", processed_date_end))


def process_quantative_values_semantics(
    ai: str, val: str, rdf_subject: str, digital_link: DigitalLink
):
    semantics = QUANTATIVE_VALUES_SEMANTICS[ai[:3]]
    properties = semantics["properties"]
    rec_20 = semantics["rec_20"]
    processed_value = int(val) / pow(10, int(ai[3]))

    rdf_node_type = RDF(BLANK_NODE, "rdf:type", "gs1:QuantativeValue")
    rdf_node_unit_code = RDF(BLANK_NODE, "gs1:unitCode", rec_20)
    rdf_node_value = RDF(BLANK_NODE, "gs1:value", processed_value)

    for property in properties:
        digital_link.add_rdf(
            RDF(
                rdf_subject,
                property,
                [rdf_node_type, rdf_node_unit_code, rdf_node_value],
            )
        )


def extract_semantics(ai: str, val: str, rdf_subject: str, digital_link: DigitalLink):
    if ai in STRING_SEMANTICS:
        process_string_semantics(ai, val, rdf_subject, digital_link)
    elif ai in DATE_SEMANTICS:
        process_date_semantics(ai, val, rdf_subject, digital_link)
    elif ai in DATETIME_MIN_SEMANTICS:
        process_datetime_min_semantics(ai, val, rdf_subject, digital_link)
    elif ai in DATETIME_SEC_SEMANTICS:
        process_datetime_sec_semantics(ai, val, rdf_subject, digital_link)
    elif ai in DATE_RANGE_SEMANTICS:
        process_date_range_semantics(ai, val, rdf_subject, digital_link)
    elif ai[:3] in QUANTATIVE_VALUES_SEMANTICS:
        process_quantative_values_semantics(ai, val, rdf_subject, digital_link)
