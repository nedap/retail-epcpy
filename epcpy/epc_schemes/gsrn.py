import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    encode_partition_table,
    str_to_binary,
)
from epcpy.utils.regex import GSRN_URI

GSRN_URI_REGEX = re.compile(GSRN_URI)


PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 18,
        "K": 5,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 21,
        "K": 6,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 24,
        "K": 7,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 28,
        "K": 8,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 31,
        "K": 9,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 34,
        "K": 10,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 38,
        "K": 11,
    },
}

PARTITION_TABLE_L = {
    12: PARTITION_TABLE_P[0],
    11: PARTITION_TABLE_P[1],
    10: PARTITION_TABLE_P[2],
    9: PARTITION_TABLE_P[3],
    8: PARTITION_TABLE_P[4],
    7: PARTITION_TABLE_P[5],
    6: PARTITION_TABLE_P[6],
}


class GSRNFilterValues(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GSRN(EPCScheme, TagEncodable, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GSRN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid GSRN URI {epc_uri}")

        self._company_pref, self._service_ref = epc_uri.split(":")[4].split(".")

        if len(f"{self._company_pref}{self._service_ref}") != 17 or not (
            6 <= len(self._company_pref) <= 12
        ):
            raise ConvertException(
                message=f"Invalid EPC URI {epc_uri} | wrong number of digits"
            )

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._service_ref}")

        self._gsrn = f"{self._company_pref}{self._service_ref}{check_digit}"

    def gs1_key(self) -> str:
        return self._gsrn

    def gs1_element_string(self) -> str:
        return f"(8018){self._gsrn}"

    def tag_uri(self, filter_value: GSRNFilterValues) -> str:
        if filter_value is None and self._tag_uri is None:
            raise ConvertException(
                message="Either tag_uri should be set or a filter value should be provided"
            )
        elif self._tag_uri:
            return self._tag_uri

        scheme = BinaryCodingSchemes.GSRN_96.value
        filter_val = filter_value.value

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._service_ref}"

        return self._tag_uri

    def binary(self, filter_value: GSRNFilterValues = None) -> str:
        if filter_value is None and self._binary:
            return self._binary

        self.tag_uri(filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._service_ref]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        gsrn_binary = encode_partition_table(parts, PARTITION_TABLE_L)

        self._binary = header + filter_binary + gsrn_binary + "0" * 24
        return self._binary


def binary_to_value_gsrn96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    gsrn_binary = truncated_binary[11:72]

    filter_string = binary_to_int(filter_binary)
    gsrn_string = decode_partition_table(gsrn_binary, PARTITION_TABLE_P)

    return f"{filter_string}.{gsrn_string}"


def tag_to_value_gsrn96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
