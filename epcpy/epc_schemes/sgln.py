from __future__ import annotations

import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_partition_table,
    decode_string,
    encode_partition_table,
    encode_string,
    parse_header_and_truncate_binary,
    replace_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from epcpy.utils.regex import SGLN_URI

SGLN_URI_REGEX = re.compile(SGLN_URI)

PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 1,
        "K": 0,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 4,
        "K": 1,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 7,
        "K": 2,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 11,
        "K": 3,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 14,
        "K": 4,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 17,
        "K": 5,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 21,
        "K": 6,
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


class SGLNFilterValue(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class SGLN(EPCScheme, TagEncodable, GS1Keyed):
    class BinaryCodingScheme(Enum):
        SGLN_96 = "sgln-96"
        SGLN_195 = "sgln-195"

    class BinaryHeader(Enum):
        SGLN_96 = "00110010"
        SGLN_195 = "00111001"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SGLN_URI_REGEX.fullmatch(epc_uri):
            raise ConvertException(message=f"Invalid SGLN URI {epc_uri}")

        self._company_pref, self._location_ref = epc_uri.split(":")[4].split(".")[:2]
        self._serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])

        if (
            len(f"{self._company_pref}{self._location_ref}") != 12
            or not (6 <= len(self._company_pref) <= 12)
            or len(replace_uri_escapes(self._serial)) > 20
        ):
            raise ConvertException(
                message=f"Invalid SGLN URI {epc_uri} | Company prefix + location reference must be 12 digits"
            )

        verify_gs3a3_component(self._serial)

        self.epc_uri = epc_uri

        check_digit = calculate_checksum(f"{self._company_pref}{self._location_ref}")
        self._gln = f"{self._company_pref}{self._location_ref}{check_digit}"

    def gs1_key(self) -> str:
        return self._gln

    def gs1_element_string(self) -> str:
        extension = replace_uri_escapes(self._serial)
        ext = "" if extension == "0" else f"(254){extension}"

        return f"(414){self._gln}{ext}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingScheme, filter_value: SGLNFilterValue
    ) -> str:

        if (
            binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_195
            and len(replace_uri_escapes(self._serial)) > 20
        ) or (
            binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_96
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 41)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        return f"{self.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_value.value}.{self._company_pref}.{self._location_ref}.{self._serial}"

    def binary(
        self,
        filter_value: SGLNFilterValue,
        binary_coding_scheme: BinaryCodingScheme,
    ) -> str:

        parts = [self._company_pref, self._location_ref]

        header = SGLN.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value.value, 3)
        gln_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(self._serial, 41)
            if binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_96
            else encode_string(self._serial, 140)
        )

        return header + filter_binary + gln_binary + serial_binary

    @classmethod
    def from_binary(cls, binary_string: str) -> SGLN:
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            cls.header_to_schemes(),
        )

        filter_binary = truncated_binary[8:11]
        gln_binary = truncated_binary[11:55]
        serial_binary = truncated_binary[55:]

        filter_string = binary_to_int(filter_binary)
        gln_string = decode_partition_table(gln_binary, PARTITION_TABLE_P)
        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == SGLN.BinaryCodingScheme.SGLN_96
            else decode_string(serial_binary)
        )

        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gln_string}.{serial_string}"
        )
