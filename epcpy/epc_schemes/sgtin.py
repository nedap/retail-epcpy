from __future__ import annotations
import re
from enum import Enum, IntEnum

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
from epcpy.utils.regex import SGTIN_URI, TAG_URI

SGTIN_REGEX = re.compile(SGTIN_URI)
TAG_URI_REGEX = re.compile(TAG_URI)

PARTITION_TABLE_P = {
    0: {
        "P": 0,
        "M": 40,
        "L": 12,
        "N": 4,
        "K": 1,
    },
    1: {
        "P": 1,
        "M": 37,
        "L": 11,
        "N": 7,
        "K": 2,
    },
    2: {
        "P": 2,
        "M": 34,
        "L": 10,
        "N": 10,
        "K": 3,
    },
    3: {
        "P": 3,
        "M": 30,
        "L": 9,
        "N": 14,
        "K": 4,
    },
    4: {
        "P": 4,
        "M": 27,
        "L": 8,
        "N": 17,
        "K": 5,
    },
    5: {
        "P": 5,
        "M": 24,
        "L": 7,
        "N": 20,
        "K": 6,
    },
    6: {
        "P": 6,
        "M": 20,
        "L": 6,
        "N": 24,
        "K": 7,
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


class SGTINFilterValues(Enum):
    ALL_OTHERS = "0"
    POS_ITEM = "1"
    FULL_CASE = "2"
    RESERVED_3 = "3"
    INNER_PACK = "4"
    RESERVED_5 = "5"
    UNIT_LOAD = "6"
    COMPONENT = "7"


class GTIN_TYPE(IntEnum):
    GTIN8 = (8,)
    GTIN12 = (12,)
    GTIN13 = (13,)
    GTIN14 = 14


class BinaryCodingSchemes(Enum):
    SGTIN_96 = "sgtin-96"
    SGTIN_198 = "sgtin-198"


class BinaryHeaders(Enum):
    SGTIN_96 = "00110000"
    SGTIN_198 = "00110110"


class SGTIN(EPCScheme, TagEncodable, GS1Keyed):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not SGTIN_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid SGTIN URI {epc_uri}")

        if len("".join(epc_uri.split(":")[4].split(".")[:2])) != 13:
            raise ConvertException(
                message=f"Invalid SGTIN URI {epc_uri} | Company prefix + item reference must be 13 digits"
            )

        serial = ".".join(":".join(epc_uri.split(":")[4:]).split(".")[2:])
        verify_gs3a3_component(serial)

        if not (1 <= len(replace_uri_escapes(serial)) <= 20):
            raise ConvertException(
                message=f"Invalid number of characters in serial: {len(replace_uri_escapes(serial))}"
            )

        self.epc_uri = epc_uri

        value = self.epc_uri.split(":")[4]
        self._company_pref = value.split(".")[0]
        self._item_ref = value.split(".")[1]
        check_digit = calculate_checksum(
            f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}"
        )

        self._serial = serial
        self._gtin = f"{self._item_ref[0]}{self._company_pref}{self._item_ref[1:]}{check_digit}".zfill(
            14
        )

    @classmethod
    def from_epc_uri(cls, epc_uri: str) -> SGTIN:
        return cls(epc_uri)

    @classmethod
    def from_gtin_plus_serial(cls, gtin: str, serial: str) -> SGTIN:
        # todo: is this always valid? maybe first validate gtin
        gtin = gtin.zfill(14)
        return cls(f"urn:epc:id:sgtin:{gtin[1:8]}.{gtin[0]}{gtin[8:13]}.{str(serial)}")

    @classmethod
    def from_tag_uri(cls, epc_tag_uri: str) -> SGTIN:
        if not TAG_URI_REGEX.match(epc_tag_uri):
            raise ConvertException(message=f"Invalid EPC tag URI {epc_tag_uri}")

        epc_scheme = epc_tag_uri.split(":")[3]
        value = ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])

        return f"urn:epc:id:{epc_scheme.split('-')[0]}:{value}"

    def gs1_key(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        return self.gtin(gtin_type=gtin_type)

    def gtin(self, gtin_type=GTIN_TYPE.GTIN14) -> str:
        if gtin_type != GTIN_TYPE.GTIN14:
            if not self._gtin.startswith((14 - gtin_type) * "0"):
                raise ConvertException(message=f"Invalid GTIN{gtin_type}")

        return self._gtin[14 - gtin_type : 14]

    def gs1_element_string(self) -> str:
        gtin = self._gtin
        serial = replace_uri_escapes(self._serial)

        return f"(01){gtin}(21){serial}"

    def tag_uri(
        self,
        binary_coding_scheme: BinaryCodingSchemes = BinaryCodingSchemes.SGTIN_96,
        filter_value: SGTINFilterValues = SGTINFilterValues.POS_ITEM,
    ) -> str:

        scheme = binary_coding_scheme.value
        filter_val = filter_value.value

        return f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._item_ref}.{self._serial}"

    def binary(
        self,
        binary_coding_scheme: BinaryCodingSchemes = BinaryCodingSchemes.SGTIN_96,
        filter_value: SGTINFilterValues = SGTINFilterValues.POS_ITEM,
    ) -> str:

        tag_uri = self.tag_uri(binary_coding_scheme, filter_value)

        scheme = tag_uri.split(":")[3]
        filter_value = tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._item_ref]

        header = BinaryHeaders[binary_coding_scheme.name].value
        filter_binary = str_to_binary(filter_value, 3)
        gtin_binary = encode_partition_table(parts, PARTITION_TABLE_L)

        serial_binary = (
            str_to_binary(self._serial, 38)
            if scheme == BinaryCodingSchemes.SGTIN_96.value
            else encode_string(self._serial, 140)
        )

        _binary = header + filter_binary + gtin_binary + serial_binary
        return _binary

    @classmethod
    def from_binary(cls, binary_string: str):
        binary_coding_scheme, truncated_binary = parse_header_and_truncate_binary(
            binary_string,
            {
                BinaryHeaders.SGTIN_96.value: BinaryCodingSchemes.SGTIN_96,
                BinaryHeaders.SGTIN_198.value: BinaryCodingSchemes.SGTIN_198,
            },
        )

        filter_binary = truncated_binary[8:11]
        gtin_binary = truncated_binary[11:58]
        serial_binary = truncated_binary[58:]

        filter_string = binary_to_int(filter_binary)
        gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)

        if binary_coding_scheme == BinaryCodingSchemes.SGTIN_96.value:
            return cls.from_tag_uri(
                f"urn:epc:tag:{binary_coding_scheme.value}:{filter_string}.{gtin_string}.{binary_to_int(serial_binary)}"
            )
        else:
            return cls.from_tag_uri(
                f"urn:epc:tag:{binary_coding_scheme.value}:{filter_string}.{gtin_string}.{decode_string(serial_binary)}"
            )

    def tag_to_value_sgtin(epc_tag_uri: str) -> str:
        return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
