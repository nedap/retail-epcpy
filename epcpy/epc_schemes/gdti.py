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
from epcpy.utils.regex import GDTI_URI

GDTI_URI_REGEX = re.compile(GDTI_URI)

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


class GDTIFilterValue(Enum):
    ALL_OTHERS = "0"
    TRAVEL_DOCUMENT = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class GDTI(EPCScheme, TagEncodable, GS1Keyed):
    class BinaryCodingScheme(Enum):
        GDTI_96 = "gdti-96"
        GDTI_174 = "gdti-174"

    class BinaryHeader(Enum):
        GDTI_96 = "00101100"
        GDTI_174 = "00111110"

    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not GDTI_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid GDTI URI {epc_uri}")

        if len("".join(epc_uri.split(":")[4].split(".")[:2])) != 12:
            raise ConvertException(
                message=f"Invalid GDTI URI {epc_uri} | Company prefix + document type must be 12 digits"
            )

        serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(serial)

        self.epc_uri = epc_uri

        self._company_pref, self._doc_type = epc_uri.split(":")[4].split(".")[:2]
        check_digit = calculate_checksum(f"{self._company_pref}{self._doc_type}")

        self._serial = serial
        self._gdti = f"{self._company_pref}{self._doc_type}{check_digit}{replace_uri_escapes(serial)}"

    def gs1_key(self) -> str:
        return self._gdti

    def gs1_element_string(self) -> str:
        return f"(253){self._gdti}"

    def tag_uri(
        self,
        binary_coding_scheme: GDTI.BinaryCodingScheme,
        filter_value: GDTIFilterValue,
    ) -> str:
        scheme = binary_coding_scheme.value
        filter_val = filter_value.value

        if (
            scheme == GDTI.BinaryCodingScheme.GDTI_174.value
            and len(replace_uri_escapes(self._serial)) > 17
        ) or (
            scheme == GDTI.BinaryCodingScheme.GDTI_96.value
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 41)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._doc_type}.{self._serial}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingScheme,
        filter_value: GDTIFilterValue,
    ) -> str:

        tag_uri = self.tag_uri(binary_coding_scheme, filter_value)

        scheme = tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._doc_type]

        header = GDTI.BinaryHeader[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value, 3)
        gdti_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        serial_binary = (
            str_to_binary(self._serial, 41)
            if scheme == "GDTI_96"
            else encode_string(self._serial, 119)
        )

        _binary = header + filter_binary + gdti_binary + serial_binary
        return _binary

    @classmethod
    def from_binary(cls, binary_string: str) -> GDTI:
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            {
                GDTI.BinaryHeader.GDTI_96.value: GDTI.BinaryCodingScheme.GDTI_96,
                GDTI.BinaryHeader.GDIT_174.value: GDTI.BinaryCodingScheme.GDTI_174,
            },
        )

        filter_binary = truncated_binary[8:11]
        gdti_binary = truncated_binary[11:55]
        serial_binary = truncated_binary[55:]

        filter_string = binary_to_int(filter_binary)
        gdti_string = decode_partition_table(gdti_binary, PARTITION_TABLE_P)

        serial_string = (
            binary_to_int(serial_binary)
            if binary_coding_scheme == GDTI.BinaryCodingScheme.GDTI_96.value
            else decode_string(serial_binary)
        )
        return cls.from_tag_uri(
            f"{cls.TAG_URI_PREFIX}{binary_coding_scheme.value}:{filter_string}.{gdti_string}.{serial_string}"
        )
