import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, TagEncodable
from epcpy.utils.common import (
    BinaryCodingSchemes,
    BinaryHeaders,
    ConvertException,
    binary_to_int,
    calculate_checksum,
    decode_fixed_width_integer,
    decode_partition_table,
    decode_string,
    encode_fixed_width_integer,
    encode_partition_table,
    encode_string,
    replace_uri_escapes,
    str_to_binary,
    verify_gs3a3_component,
)
from epcpy.utils.regex import ITIP_URI

ITIP_URI_REGEX = re.compile(ITIP_URI)

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


class ITIPFilterValues(Enum):
    ALL_OTHERS = "0"
    RESERVED_1 = "1"
    RESERVED_2 = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    RESERVED_6 = "6"
    RESERVED_7 = "7"


class ITIP(EPCScheme, TagEncodable):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not ITIP_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid ITIP URI {epc_uri}")

        company_prefix, item_ref, piece, total, *serial = ":".join(
            epc_uri.split(":")[4:]
        ).split(".")

        serial = ".".join(serial)
        verify_gs3a3_component(serial)

        if len(f"{company_prefix}{item_ref}{piece}{total}") != 17:
            raise ConvertException(
                message=f"Invalid ITIP URI {epc_uri} | first four components must be 17 digits"
            )

        if not (1 <= len(serial) <= 20):
            raise ConvertException(
                message=f"Invalid serial | serial must be between 1 and 20 digits"
            )

        self.epc_uri = epc_uri

        self._company_pref = company_prefix
        self._item_ref = item_ref
        self._piece = piece
        self._total = total
        self._serial = serial

    def gs1_element_string(self) -> str:
        indicator = self._item_ref[0]

        check_digit = calculate_checksum(
            f"{indicator}{self._company_pref}{self._item_ref[1:]}"
        )
        return f"(8006){indicator}{self._company_pref}{self._item_ref[1:]}{check_digit}{self._piece}{self._total}(21){replace_uri_escapes(self._serial)}"

    def tag_uri(
        self, binary_coding_scheme: BinaryCodingSchemes, filter_value: ITIPFilterValues
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
            scheme == BinaryCodingSchemes.ITIP_212.value
            and len(replace_uri_escapes(self._serial)) > 20
        ) or (
            scheme == BinaryCodingSchemes.ITIP_110.value
            and (
                not self._serial.isnumeric()
                or int(self._serial) >= pow(2, 38)
                or (len(self._serial) > 1 and self._serial[0] == "0")
            )
        ):
            raise ConvertException(message=f"Invalid serial value {self._serial}")

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._company_pref}.{self._item_ref}.{self._piece}.{self._total}.{self._serial}"

        return self._tag_uri

    def binary(
        self,
        binary_coding_scheme: BinaryCodingSchemes = None,
        filter_value: ITIPFilterValues = None,
    ) -> str:
        if (binary_coding_scheme is None or filter_value is None) and self._binary:
            return self._binary

        self.tag_uri(binary_coding_scheme, filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_value = self._tag_uri.split(":")[4].split(".")[0]
        parts = [self._company_pref, self._item_ref]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_value, 3)
        gtin_binary = encode_partition_table(parts, PARTITION_TABLE_L)
        piece_binary = encode_fixed_width_integer(self._piece, 7)
        total_binary = encode_fixed_width_integer(self._total, 7)
        serial_binary = (
            str_to_binary(self._serial, 38)
            if scheme == "ITIP_110"
            else encode_string(self._serial, 140)
        )

        _binary = (
            header
            + filter_binary
            + gtin_binary
            + piece_binary
            + total_binary
            + serial_binary
        )
        return _binary


def binary_to_value_itip110(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    gtin_binary = truncated_binary[11:58]
    piece_binary = truncated_binary[58:65]
    total_binary = truncated_binary[65:72]
    serial_binary = truncated_binary[72:]

    filter_string = binary_to_int(filter_binary)
    gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)
    piece_string = decode_fixed_width_integer(piece_binary)
    total_string = decode_fixed_width_integer(total_binary)
    serial_string = binary_to_int(serial_binary)

    return (
        f"{filter_string}.{gtin_string}.{piece_string}.{total_string}.{serial_string}"
    )


def binary_to_value_itip212(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:11]
    gtin_binary = truncated_binary[11:58]
    piece_binary = truncated_binary[58:65]
    total_binary = truncated_binary[65:72]
    serial_binary = truncated_binary[72:]

    filter_string = binary_to_int(filter_binary)
    gtin_string = decode_partition_table(gtin_binary, PARTITION_TABLE_P)
    piece_string = decode_fixed_width_integer(piece_binary)
    total_string = decode_fixed_width_integer(total_binary)
    serial_string = decode_string(serial_binary)

    return (
        f"{filter_string}.{gtin_string}.{piece_string}.{total_string}.{serial_string}"
    )


def tag_to_value_itip110(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])


def tag_to_value_itip212(epc_tag_uri: str) -> str:
    return ".".join(":".join(epc_tag_uri.split(":")[3:]).split(".")[1:])
