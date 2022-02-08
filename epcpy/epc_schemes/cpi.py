import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    decode_partition_table,
    encode_partition_table,
    str_to_binary,
)
from epcpy.utils.regex import CPI_URI

CPI_URI_REGEX = re.compile(CPI_URI)
PARTITION_TABLE_P_96 = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 11,
        "K": 3,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 14,
        "K": 4,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 17,
        "K": 5,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 21,
        "K": 6,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 24,
        "K": 7,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 27,
        "K": 8,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 31,
        "K": 9,
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

PARTITION_TABLE_P_VAR = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 114,
        "K": 18,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 120,
        "K": 19,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 126,
        "K": 20,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 132,
        "K": 21,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 138,
        "K": 22,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 144,
        "K": 23,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 150,
        "K": 24,
    },
}

PARTITION_TABLE_L_VAR = {
    12: PARTITION_TABLE_P_VAR[0],
    11: PARTITION_TABLE_P_VAR[1],
    10: PARTITION_TABLE_P_VAR[2],
    9: PARTITION_TABLE_P_VAR[3],
    8: PARTITION_TABLE_P_VAR[4],
    7: PARTITION_TABLE_P_VAR[5],
    6: PARTITION_TABLE_P_VAR[6],
}


class CPIFilterValues(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


def replace_cpi_escapes(cpi: str) -> str:
    return cpi.replace("%23", "#").replace("%2F", "/")


class BinaryCodingSchemes(Enum):
    pass


class CPI(EPCScheme, TagEncodable):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not CPI_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid CPI URI {epc_uri}")

        self._company_pref, self._cp_ref, self._serial = epc_uri.split(":")[4].split(
            "."
        )

        if (
            len("".join([self._company_pref, self._cp_ref])) > 30
            or len(self._serial) > 12
        ):
            raise ConvertException(
                message=f"Invalid CPI URI {epc_uri} | wrong number of characters"
            )

        self.epc_uri = epc_uri

    def gs1_element_string(self) -> str:
        cp_ref = replace_cpi_escapes(self._cp_ref)

        return f"(8010){self._company_pref}{cp_ref}(8011){self._serial}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes, filter_value: CPIFilterValues
    ) -> str:
        if (
            binary_coding_scheme is None or filter_value is None
        ) and self._tag_uri is None:
            raise ConvertException(
                message="Either both a binary coding scheme and a filter value should be provided, or tag_uri should be set."
            )
        elif self._tag_uri:
            return self._tag_uri

        scheme = binary_coding_scheme.value
        filter_val = filter_value.value

        if (
            scheme == BinaryCodingSchemes.CPI_VAR.value
            and len(self._serial) > 12
            or (len(self._serial) > 1 and self._serial[0] == "0")
        ) or (
            scheme == BinaryCodingSchemes.CPI_96.value
            and (
                int(self._serial) >= pow(2, 31)
                or (len(self._serial) > 1 and self._serial[0] == "0")
                or not self._cp_ref.isnumeric()
                or (len(self._cp_ref) > 1 and self._cp_ref[0] == "0")
                or len(self._cp_ref) > 15 - len(self._company_pref)
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._cp_ref}.{self._serial}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingSchemes = None,
        filter_value: CPIFilterValues = None,
    ) -> str:
        if (binary_coding_scheme is None or filter_value is None) and self._binary:
            return self._binary

        self.tag_uri(binary_coding_scheme, filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._cp_ref]
        serial = self._serial

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        cpi_binary = (
            encode_partition_table(parts, PARTITION_TABLE_L_96)
            if scheme == "CPI_96"
            else encode_partition_table(
                parts, PARTITION_TABLE_L_VAR, six_bit_variable_partition=True
            )
        )
        serial_binary = str_to_binary(serial, 31 if scheme == "CPI_96" else 40)

        _binary = header + filter_binary + cpi_binary + serial_binary

        return _binary


def binary_to_value_cpi96(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    cpi_binary = truncated_binary[11:65]
    serial_binary = truncated_binary[65:]

    filter_string = binary_to_int(filter_binary)
    cpi_string = decode_partition_table(
        cpi_binary, PARTITION_TABLE_P_96, unpadded_partition=True
    )
    serial_string = binary_to_int(serial_binary)

    return f"{filter_string}.{cpi_string}.{serial_string}"


def binary_to_value_cpivar(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    cpi_binary = truncated_binary[11:-40]
    serial_binary = truncated_binary[-40:]

    filter_string = binary_to_int(filter_binary)
    cpi_string = decode_partition_table(
        cpi_binary, PARTITION_TABLE_P_VAR, six_bit_variable_partition=True
    )
    serial_string = binary_to_int(serial_binary)

    return f"{filter_string}.{cpi_string}.{serial_string}"


def tag_to_value_cpi96(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])


def tag_to_value_cpivar(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
