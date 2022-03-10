from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    NoGS1KeyException,
    binary_to_int,
    decode_partition_table,
    encode_partition_table,
    parse_header_and_truncate_binary,
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


class CPIFilterValue(Enum):
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


class CPI(EPCScheme, GS1Keyed, TagEncodable):
    class BinaryCodingScheme(Enum):
        CPI_96 = "cpi-96"
        CPI_VAR = "cpi-var"

    class BinaryHeader(Enum):
        CPI_96 = "00111100"
        CPI_VAR = "00111101"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not CPI_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid CPI URI {epc_uri}")

        self._company_pref, self._cp_ref, self._serial = epc_uri.split(":")[4].split(
            "."
        )

        if (
            len("".join([self._company_pref, self._cp_ref])) > 30
            or len(self._serial) > 12
            or not (6 <= len(self._company_pref) <= 12)
        ):
            raise ConvertException(message=f"Invalid CPI URI {epc_uri}")

        self.epc_uri = epc_uri

    def gs1_key(self) -> None:
        raise NoGS1KeyException(message="CPI has no GS1 key, only a GS1 element string")

    def gs1_element_string(self) -> str:
        cp_ref = replace_cpi_escapes(self._cp_ref)

        return f"(8010){self._company_pref}{cp_ref}(8011){self._serial}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: CPIFilterValue
    ) -> str:

        if (
            binary_coding_scheme == CPI.BinaryCodingScheme.CPI_VAR
            and len(self._serial) > 12
        ) or (
            binary_coding_scheme == CPI.BinaryCodingScheme.CPI_96
            and (
                int(self._serial) >= pow(2, 31)
                or not self._cp_ref.isnumeric()
                or (len(self._cp_ref) > 1 and self._cp_ref[0] == "0")
                or len(self._cp_ref) > 15 - len(self._company_pref)
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        self._tag_uri = f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_value.value}.{self._company_pref}.{self._cp_ref}.{self._serial}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: CPIFilterValue,
    ) -> str:

        parts = [self._company_pref, self._cp_ref]
        serial = self._serial

        header = CPI.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        cpi_binary = (
            encode_partition_table(parts, PARTITION_TABLE_L_96)
            if binary_coding_scheme == CPI.BinaryCodingScheme.CPI_96
            else encode_partition_table(
                parts, PARTITION_TABLE_L_VAR, six_bit_variable_partition=True
            )
        )
        serial_binary = str_to_binary(
            serial, 31 if binary_coding_scheme == CPI.BinaryCodingScheme.CPI_96 else 40
        )

        _binary = header + filter_binary + cpi_binary + serial_binary

        return _binary

    @classmethod
    def from_binary(cls, binary_string: str) -> CPI:
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )
        filter_binary = truncated_binary[8:11]

        if binary_coding_scheme == CPI.BinaryCodingScheme.CPI_96:
            cpi_binary = truncated_binary[11:65]
            serial_binary = truncated_binary[65:]
            cpi_string = decode_partition_table(
                cpi_binary, PARTITION_TABLE_P_96, unpadded_partition=True
            )
        else:
            cpi_binary = truncated_binary[11:]

            cpi_string = decode_partition_table(
                cpi_binary, PARTITION_TABLE_P_VAR, six_bit_variable_partition=True
            )

            partition = PARTITION_TABLE_P_VAR[binary_to_int(cpi_binary[:3])]
            possible_serial_binary = truncated_binary[(11 + 3 + partition["M"]) :]

            serial_binary = ""
            is_serial = False
            for g in re.split("([0-1]{6})", possible_serial_binary):
                if is_serial:
                    serial_binary += g
                if g == "000000":
                    is_serial = True

            serial_binary = serial_binary[:40] if len(serial_binary) > 0 else "0"

        filter_string = binary_to_int(filter_binary)
        serial_string = binary_to_int(serial_binary)

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{cpi_string}.{serial_string}"
        )
