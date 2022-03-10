from typing import List

BLANK_NODE = None


class RDF:
    def __init__(self, subject, predicate, obj) -> None:
        super().__init__()

        self.subject = subject
        self.predicate = predicate
        self.object = obj


class DigitalLink:
    def __init__(self, digital_link_uri: str) -> None:
        super().__init__()

        self.digital_link_uri = digital_link_uri
        self.rdfs: List[RDF] = []

    def add_rdf(self, rdf: RDF) -> None:
        self.rdfs.append(rdf)
