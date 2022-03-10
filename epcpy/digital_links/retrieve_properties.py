import re
from typing import List

from epcpy.digital_links.model import BLANK_NODE, RDF, DigitalLink
from epcpy.digital_links.regex import (
    CUSTOM_URI_STEM,
    GS1PATH,
    QUERY_STRING_COMP,
    QUERY_STRING_DELIM,
    UNCOMPRESSED_CUSTOM_GS1_WEB_URI,
)
from epcpy.digital_links.semantic_extraction import extract_semantics

URI_STEM_REGEX = re.compile(CUSTOM_URI_STEM)
GS1PATH_REGEX = re.compile(GS1PATH)
QUERY_STRING_REGEX = re.compile(QUERY_STRING_COMP)
QUERY_STRING_DELIM_REGEX = re.compile(QUERY_STRING_DELIM)
WEB_URI = re.compile(UNCOMPRESSED_CUSTOM_GS1_WEB_URI)

INSTANCE_IDENTIFIERS = {
    "01": {
        "additional_ais": ["21", "235"],
    },
    "00": {"additional_ais": None},
    "253": {
        "min_length": 14,
    },
    "254": {
        "min_length": 14,
    },
    "8003": {
        "min_length": 15,
    },
    "8004": {"additional_ais": None},
    "8006": {
        "additional_ais": ["21"],
    },
    "8010": {"additional_ais": ["8011"]},
}

CLASS_SEMANTICS = {
    "01": ["gs1:Product", "schema:Product"],
    "8006": ["gs1:Product", "schema:Product"],
    "414": ["gs1:Place", "schema:Place"],
    "417": ["gs1:Organization", "schema:Organization"],
}


def determine_instance(ai: str, value: str, other_ais: List[str]) -> bool:
    if ai not in INSTANCE_IDENTIFIERS:
        return False

    row = INSTANCE_IDENTIFIERS[ai]

    # Check valid length
    if "min_length" in row:
        return len(value) >= row["min_length"]

    if "additional_ais" not in row:
        return False

    additional_ais = row["additional_ais"]

    # No required additional AIs
    if additional_ais is None:
        return True

    # Is at least one of the required additional AIs present
    return len(set(additional_ais) - set(other_ais)) < len(additional_ais)


def process_class_semantics(ai: str, rdf_subject: str, digital_link: DigitalLink):
    if ai not in CLASS_SEMANTICS:
        return

    for cls in CLASS_SEMANTICS[ai]:
        digital_link.add_rdf(RDF(rdf_subject, "rdf:type", cls))


def process_subclasses(
    U: str, gs1_path: str, is_instance: bool, digital_link: DigitalLink
):
    tmp_path = gs1_path
    count = 1
    while len(tmp_path.split("/")) >= 4:
        new_U = "/".join(U.split("/")[: -count * 2])

        if not re.match(WEB_URI, new_U):
            return

        digital_link.add_rdf(RDF(U, "rdfs:subClassOf", new_U))
        digital_link.add_rdf(RDF(U, "dcterms:isPartOf", new_U))

        if count == 1 and is_instance:
            digital_link.add_rdf(RDF(U, "rdf:type", new_U))

        tmp_path = "/".join(gs1_path.split("/")[: -count * 2])
        count += 1


def retrieve_properties(digital_link_uri: str) -> DigitalLink:
    digital_link = DigitalLink(digital_link_uri)

    # Assumes digital link is validated
    gs1_path = re.search(GS1PATH, digital_link_uri).group(0)
    query_string = re.search(QUERY_STRING_REGEX, digital_link_uri)

    # Ignore first /
    _, ai, val, *others = gs1_path.split("/")
    additional_ais = others[::2]

    is_instance = determine_instance(ai, val, additional_ais)

    U = digital_link_uri[: -len(query_string.group(0)) if query_string else None]
    rdf_subject = BLANK_NODE if not is_instance and query_string else U

    process_class_semantics(ai, rdf_subject, digital_link)

    all_ai = gs1_path[1:].split("/")[0::2]
    all_ai_vals = gs1_path[1:].split("/")[1::2]

    if query_string:
        query_string_components = [
            x
            for x in re.split(QUERY_STRING_DELIM_REGEX, query_string.group(0)[1:])
            if x not in ["&", ";"]
        ]
        for comp in query_string_components:
            k, v = comp.split("=")
            all_ai.append(k)
            all_ai_vals.append(v)

    for ai_key, value in zip(all_ai, all_ai_vals):
        extract_semantics(ai_key, value, rdf_subject, digital_link)

    process_subclasses(U, gs1_path[1:], is_instance, digital_link)

    return digital_link
