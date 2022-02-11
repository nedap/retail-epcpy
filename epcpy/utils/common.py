import base64
import re
from enum import Enum
from math import inf, log
from typing import Dict, Tuple

from epcpy.utils.regex import VERIFY_GS3A3_CHARS


ESCAPE_CHARACTERS = {
    "0100010": "%22",
    "0100101": "%25",
    "0100110": "%26",
    "0101111": "%2F",
    "0111100": "%3C",
    "0111110": "%3E",
    "0111111": "%3F",
}


VERIFY_GS3A3_CHARS_REGEX = re.compile(VERIFY_GS3A3_CHARS)


class ConvertException(Exception):
    def __init__(self, *args: object, message="") -> None:
        self.message = message
        super().__init__(self.message, *args)


def ignore_errors_during_conversion(func, *args, **kwargs):
    try:
        return func(*args, **kwargs)
    except ConvertException:
        return None


def replace_uri_escapes(uri: str) -> str:
    return (
        uri.replace("%22", '"')
        .replace("%26", "&")
        .replace("%2F", "/")
        .replace("%3C", "<")
        .replace("%3E", ">")
        .replace("%3F", "?")
        .replace("%25", "%")
    )


def int_to_binary(integer: int, num_bits: int) -> str:
    return f"{integer:0{num_bits}b}"


def binary_to_int(binary: str) -> int:
    return int(binary, 2)


def str_to_binary(string: str, num_bits: int) -> str:
    return int_to_binary(int(string), num_bits)


def base64_to_hex(base64_string: str) -> str:
    # Add padding to ensure valid padding
    return base64.b64decode(f"{base64_string}==").hex()


def hex_to_base64(hex_string: str) -> str:
    return base64.b64encode(bytes.fromhex(hex_string)).decode("utf-8")


def hex_to_binary(hex_string: str) -> str:
    return f"{int(hex_string, 16):0{len(hex_string * 4)}b}"


def encode_string(string: str, num_bits: int) -> str:
    res = ""
    for g in re.split("(%[0-9a-fA-F]{2})", string):
        if len(g) == 0:
            continue
        elif g[0] != "%":
            res += "".join([str_to_binary(ord(s), 7) for s in g])
        else:
            res += str_to_binary(int(g[1:], 16), 7)
    return f"{res:<0{num_bits}}"


def decode_string_six_bits(binary: str, max_chars: int) -> str:
    res = ""
    for g in re.split("([0-1]{6})", binary):
        if g == "000000" or g == "":
            continue
        elif g.startswith("10") or g.startswith("11"):
            res += chr(int(g, 2))
        else:
            res += chr(64 + int(g, 2))

    if len(res) > max_chars:
        raise ConvertException(message="Too many characters decoded!")

    return res.replace("#", "%23").replace("/", "%2F")


def encode_string_six_bits(string: str) -> str:
    res = ""
    for g in re.split("(%[0-9a-fA-F]{2}|-)", string):
        if len(g) == 0:
            continue
        elif g == "-":
            res += "101101"
        elif g[0] != "%":
            res += "".join(
                [
                    f"11{int(s):04b}" if s.isnumeric() else f"{int(ord(s) - 64):06b}"
                    for s in g
                ]
            )
        else:
            res += str_to_binary(int(g[1:], 16), 6)
    return f"{res}000000"


def decode_binary_char(binary: str) -> str:
    if binary == "0000000":
        return ""
    elif binary in ESCAPE_CHARACTERS:
        return ESCAPE_CHARACTERS[binary]
    else:
        return chr(int(binary, 2))


def decode_string(binary: str) -> str:
    return "".join(
        list(
            map(
                decode_binary_char,
                re.findall("." * 7, binary),
            )
        )
    )


def encode_partition_table(
    parts: list[str],
    partition_table: list[dict[str, dict[str, int]]],
    string_partition=False,
    six_bit_variable_partition=False,
) -> str:
    C = parts[0]
    D = parts[1]

    partition = partition_table[len(C)]

    P_bin = int_to_binary(partition["P"], 3)
    C_bin = str_to_binary(C, partition["M"])

    if string_partition:
        D_bin = encode_string(D, partition["N"])
    elif six_bit_variable_partition:
        D_bin = encode_string_six_bits(D)
    else:
        D_bin = str_to_binary(D, partition["N"]) if partition["K"] != 0 else "0"

    return P_bin + C_bin + D_bin


def decode_partition_table(
    binary_string: str,
    partition_table: list[dict[str, dict[str, int]]],
    unpadded_partition=False,
    string_partition=False,
    six_bit_variable_partition=False,
) -> str:
    try:
        partition = partition_table[binary_to_int(binary_string[:3])]
    except KeyError:
        raise ConvertException(message=f"Invalid partition header {binary_string[:3]}")

    C = binary_to_int(binary_string[3 : (3 + partition["M"])])

    D_bin = binary_string[(3 + partition["M"]) : (3 + partition["M"] + partition["N"])]

    if string_partition:
        D = decode_string(D_bin)
    elif six_bit_variable_partition:
        D = decode_string_six_bits(D_bin, partition["K"])
    else:
        D = binary_to_int(D_bin) if partition["K"] != 0 else ""

    compare_D = not (
        unpadded_partition or string_partition or six_bit_variable_partition
    )

    if not C < pow(10, partition["L"]):
        raise ConvertException(message=f"Company prefix length too large")
    if D != "" and compare_D and not D < pow(10, partition["K"]):
        raise ConvertException(message=f"Item reference length too large")

    return f"{C:>0{partition['L']}}.{D:>0{partition['K'] if compare_D else 0}}"


def encode_numeric_string(string: str, bit_count: int) -> str:
    if 2 * pow(10, len(string)) >= pow(2, bit_count):
        raise ConvertException(message="Invalid character string")

    return str_to_binary(f"1{string}", bit_count)


def decode_numeric_string(binary: str) -> str:
    string = f"{int(binary, 2)}"

    if len(string) <= 1 or string[0] != "1":
        raise ConvertException(message="Invalid numeric string")

    return string[1:]


def encode_fixed_width_integer(string: str, bit_count: int) -> str:
    if int(string) >= (pow(10, int(bit_count * log(2) / log(10))) - 1):
        raise ConvertException(message="Fixed width numeric integer too large")

    return str_to_binary(string, bit_count)


def decode_fixed_width_integer(binary: str) -> str:
    D = int(len(binary) * log(2) / log(10))
    if int(binary, 2) > pow(10, D) - 1:
        raise ConvertException(message=f"Bits cannot be converted to {D} digits")

    return f"{int(binary, 2):0>{D}}"


def decode_cage_code(binary: str) -> str:
    return "".join(
        [chr(int(g, 2)) if g != "" else "" for g in re.split("([0-1]{8})", binary)]
    ).replace(" ", "")


def encode_cage_code(chars: str) -> str:
    return "".join([f"{ord(char):0>8b}" for char in chars])


def decode_cage_code_six_bits(binary: str) -> str:
    if binary.startswith("100000"):
        binary = binary[6:]

    return decode_string_six_bits(binary, inf)


def encode_cage_code_six_bits(chars: str) -> str:
    binary = f"{encode_string_six_bits(chars)[:-6]}"
    if len(binary) == 30:
        binary = "100000" + binary
    return binary


def verify_gs3a3_component(serial):
    res = ""
    for g in re.split("(%\d\d)", serial):
        if len(g) == 0:
            continue
        elif g[0] != "%":
            res += g
        else:
            res += chr(int(g[1:], 16))

    if not VERIFY_GS3A3_CHARS_REGEX.fullmatch(res):
        raise ConvertException()


def calculate_checksum(digits: str) -> int:
    digits = [int(d) for d in digits]
    odd, even = digits[1::2], digits[0::2]

    if len(digits) % 2 == 0:
        val1 = sum(odd)
        val2 = sum(even)
    else:
        val1 = sum(even)
        val2 = sum(odd)

    checksum = (10 - ((3 * (val1) + (val2)) % 10)) % 10

    return checksum


def parse_header_and_truncate_binary(
    binary_string: str, header_to_schemes: Dict[str, str]
) -> Tuple[str, str]:
    header = binary_string[:8]

    try:
        scheme = header_to_schemes[header]
    except ValueError:
        raise ConvertException(message=f"{header} is not a valid header")

    _, size = scheme.value.split("-")
    size = int(size) if size.isnumeric() else None

    if size and not size <= len(binary_string):
        raise ConvertException(
            message=f"Invalid binary size, expected (<=): {size} actual: {len(binary_string)}"
        )

    truncated_binary = binary_string[:size]

    return scheme, truncated_binary
