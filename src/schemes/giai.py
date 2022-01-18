import re
from enum import Enum

from base_scheme import EPC_SCHEME
from common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    decode_partition_table,
    encode_partition_table,
    replace_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from regex import GIAI_URI

GIAI_URI_REGEX = re.compile(GIAI_URI)

PARTITION_TABLE_P_96 = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 42,
        "K": 13,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 45,
        "K": 14,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 48,
        "K": 15,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 52,
        "K": 16,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 55,
        "K": 17,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 58,
        "K": 18,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 62,
        "K": 19,
    },
}

PARTITION_TABLE_L_96 = {
    12: PARTITION_TABLE_P_96[0],
    11: PARTITION_TABLE_P_96[1],
    10: PARTITION_TABLE_P_96[2],
    9: PARTITION_TABLE_P_96[3],
    8: PARTITION_TABLE_P_96[4],
    7: PARTITION_TABLE_P_96[5],
    6: PARTITION_TABLE_P_96[6],
}

PARTITION_TABLE_P_202 = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 148,
        "K": 18,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 151,
        "K": 19,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 154,
        "K": 20,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 158,
        "K": 21,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 161,
        "K": 22,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 164,
        "K": 23,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 168,
        "K": 24,
    },
}

PARTITION_TABLE_L_202 = {
    12: PARTITION_TABLE_P_202[0],
    11: PARTITION_TABLE_P_202[1],
    10: PARTITION_TABLE_P_202[2],
    9: PARTITION_TABLE_P_202[3],
    8: PARTITION_TABLE_P_202[4],
    7: PARTITION_TABLE_P_202[5],
    6: PARTITION_TABLE_P_202[6],
}


class GIAIFilterValues(Enum):
    ALL_OTHERS = "0"
    RAIL_VEHICLE = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GIAI(EPC_SCHEME):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GIAI_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid EPC URI {epc_uri}")

        company_prefix = epc_uri.split(":")[4].split(".")[0]
        if len(company_prefix) < 6 or len(company_prefix) > 12:
            raise ConvertException(
                message=f"Invalid company prefix length {len(company_prefix)}"
            )

        asset_reference = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[1:])
        verify_gs3a3_component(asset_reference)

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        company_prefix, *asset_reference = ":".join(self.epc_uri.split(":")[4:]).split(
            "."
        )

        asset_reference = replace_uri_escapes(".".join(asset_reference))

        return f"(8004){company_prefix}{asset_reference}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes, filter_value: GIAIFilterValues
    ) -> str:
        if self._tag_uri:
            return self._tag_uri

        if binary_coding_scheme is None or filter_value is None:
            raise ConvertException(
                message="Both a binary coding scheme and a filter value should be provided!"
            )

        scheme = binary_coding_scheme.value
        filter_val = filter_value.value
        value = ":".join(self.epc_uri.split(":")[4:])
        serial = ".".join(value.split(".")[1:])
        company_prefix_length = len(value.split(".")[0])

        if (
            scheme == BinaryCodingSchemes.GIAI_202.value
            and len(replace_uri_escapes(serial))
            > PARTITION_TABLE_L_202[company_prefix_length]["K"]
        ) or (
            scheme == BinaryCodingSchemes.GIAI_96.value
            and (
                not serial.isnumeric()
                or len(serial) > PARTITION_TABLE_L_96[company_prefix_length]["K"]
                or int(serial)
                >= pow(2, PARTITION_TABLE_L_96[company_prefix_length]["N"])
                or (len(serial) > 1 and serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {serial}")

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{value}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingSchemes = None,
        filter_value: GIAIFilterValues = None,
    ) -> str:
        if self._binary:
            return self._binary

        self.tag_uri(binary_coding_scheme, filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        company_prefix = self._tag_uri.split(":")[4].split(".")[1]
        asset_reference = ".".join(self._tag_uri.split(":")[4].split(".")[2:])

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)

        giai_binary = (
            encode_partition_table(
                [company_prefix, asset_reference], PARTITION_TABLE_L_96
            )
            if scheme == "GIAI_96"
            else encode_partition_table(
                [company_prefix, asset_reference],
                PARTITION_TABLE_L_202,
                string_partition=True,
            )
        )

        _binary = header + filter_binary + giai_binary
        return _binary


def binary_to_value_giai96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    giai_binary = truncated_binary[11:96]

    filter_string = binary_to_int(filter_binary)
    giai_string = decode_partition_table(
        giai_binary, PARTITION_TABLE_P_96, unpadded_partition=True
    )

    return f"{filter_string}.{giai_string}"


def binary_to_value_giai202(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    giai_binary = truncated_binary[11:202]

    filter_string = binary_to_int(filter_binary)
    giai_string = decode_partition_table(
        giai_binary, PARTITION_TABLE_P_202, string_partition=True
    )

    return f"{filter_string}.{giai_string}"


def tag_to_value_giai96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])


def tag_to_value_giai202(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
