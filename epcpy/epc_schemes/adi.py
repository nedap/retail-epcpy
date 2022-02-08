import math
import re
from enum import Enum

from epcpy.epc_schemes.base_scheme import EPCScheme, TagEncodable
from epcpy.utils.common import (
    ConvertException,
    binary_to_int,
    decode_cage_code_six_bits,
    decode_string_six_bits,
    encode_cage_code_six_bits,
    encode_string_six_bits,
    str_to_binary,
)
from epcpy.utils.regex import ADI_URI

ADI_URI_REGEX = re.compile(ADI_URI)


class ADIFilterValues(Enum):
    ALL_OTHERS = "0"
    ITEM_OTHER = "1"
    CARTON = "2"
    RESERVED_3 = "3"
    RESERVED_4 = "4"
    RESERVED_5 = "5"
    PALLET = "6"
    RESERVED_7 = "7"
    SEAT_CUSHIONS = "8"
    SEAT_COVERS = "9"
    SEAT_BELTS = "10"
    GALLEY = "11"
    UNIT_LOAD_DEVICES = "12"
    AIRCRAFT_SECURITY_ITEMS = "13"
    LIFE_VESTS = "14"
    OXYGEN_GENERATOR = "15"
    ENGINE_COMPONENTS = "16"
    AVIONICS = "17"
    EXPERIMENTAL_EQUIPMENT = "18"
    OTHER_EMERGENCY_EQUIPMENT = "19"
    OTHER_ROTABLES = "20"
    OTHER_REPAIRABLE = "21"
    OTHER_CABIN_INTERIOR = "22"
    OTHER_REPAIR = "23"
    PASSENGER_SEATS = "24"
    IFE_SYSTEMS = "25"
    RESERVED_26 = "26"
    RESERVED_27 = "27"
    RESERVED_28 = "28"
    RESERVED_29 = "29"
    RESERVED_30 = "30"
    RESERVED_31 = "31"
    RESERVED_32 = "32"
    RESERVED_33 = "33"
    RESERVED_34 = "34"
    RESERVED_35 = "35"
    RESERVED_36 = "36"
    RESERVED_37 = "37"
    RESERVED_38 = "38"
    RESERVED_39 = "39"
    RESERVED_40 = "40"
    RESERVED_41 = "41"
    RESERVED_42 = "42"
    RESERVED_43 = "43"
    RESERVED_44 = "44"
    RESERVED_45 = "45"
    RESERVED_46 = "46"
    RESERVED_47 = "47"
    RESERVED_48 = "48"
    RESERVED_49 = "49"
    RESERVED_50 = "50"
    RESERVED_51 = "51"
    RESERVED_52 = "52"
    RESERVED_53 = "53"
    RESERVED_54 = "54"
    RESERVED_55 = "55"
    LOCATION_IDENTIFIER = "56"
    DOCUMENTATION = "57"
    TOOLS = "58"
    GROUND_SUPPORT_EQUIPMENT = "59"
    OTHER_NON_FLYABLE_EQUIPMENT = "60"
    RESERVED_61 = "61"
    RESERVED_62 = "62"
    RESERVED_63 = "63"


class ADI(EPCScheme, TagEncodable):
    def __init__(self, epc_uri) -> None:
        super().__init__()

        if not ADI_URI_REGEX.match(epc_uri):
            raise ConvertException(message=f"Invalid ADI URI {epc_uri}")

        self._cage_dodaac, self._part_number, self._serial = epc_uri.split(":")[
            4
        ].split(".")

        if not (0 <= len(self._part_number.replace("%2F", "/")) <= 32):
            raise ConvertException(
                message=f"Invalid number of characters in part number: {len(self._part_number.replace('%2F', '/'))}"
            )

        if not (1 <= len(self._serial.replace("%2F", "/").replace("%23", "#")) <= 30):
            raise ConvertException(
                message=f"Invalid number of characters in serial: {len(self._serial.replace('%2F', '/').replace('%23', '#'))}"
            )

        self.epc_uri = epc_uri

    def tag_uri(self, filter_value: ADIFilterValues) -> str:
        if filter_value is None and self._tag_uri is None:
            raise ConvertException(
                message="Either tag_uri should be set or a filter value should be provided"
            )
        elif self._tag_uri:
            return self._tag_uri

        scheme = BinaryCodingSchemes.ADI_VAR.value
        filter_val = filter_value.value

        self._tag_uri = f"urn:epc:tag:{scheme}:{filter_val}.{self._cage_dodaac}.{self._part_number}.{self._serial}"

        return self._tag_uri

    def binary(self, filter_value: ADIFilterValues = None) -> str:
        if filter_value is None and self._binary:
            return self._binary

        self.tag_uri(filter_value)

        scheme = self._tag_uri.split(":")[3].replace("-", "_").upper()
        filter_val = self._tag_uri.split(":")[4].split(".")[0]

        header = BinaryHeaders[scheme].value
        filter_binary = str_to_binary(filter_val, 6)
        cage_code_binary = encode_cage_code_six_bits(self._cage_dodaac)
        part_number_binary = encode_string_six_bits(self._part_number)
        serial_binary = encode_string_six_bits(self._serial)

        self._binary = (
            header
            + filter_binary
            + cage_code_binary
            + part_number_binary
            + serial_binary
        )
        return self._binary


def binary_to_value_adivar(truncated_binary: str) -> str:
    filter_binary = truncated_binary[8:14]
    cage_code_binary = truncated_binary[14:50]

    if not re.match(".*([0]{6})+.*", truncated_binary[50:]):
        raise ConvertException(
            message="Invalid binary for ADI, missing 6-bit terminators"
        )

    part_number_binary, _, *serial_binary = re.split("([0]{6})", truncated_binary[50:])
    serial_binary = "".join(serial_binary)[:-6]

    filter_string = binary_to_int(filter_binary)
    cage_code_string = decode_cage_code_six_bits(cage_code_binary)
    part_number_string = decode_string_six_bits(part_number_binary, math.inf)
    serial_string = decode_string_six_bits(serial_binary, math.inf)

    return f"{filter_string}.{cage_code_string}.{part_number_string}.{serial_string}"


def tag_to_value_adivar(epc_tag_uri: str) -> str:
    return ".".join(epc_tag_uri.split(":")[4].split(".")[1:])
