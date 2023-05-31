import base64
import re
from enum import Enum
from math import log
from typing import Dict, List, Tuple

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
    """Custom exception class to detect failed conversions of EPCs"""

    def __init__(self, *args: object, message="") -> None:
        self.message = message
        super().__init__(self.message, *args)


def replace_uri_escapes(uri: str) -> str:
    """Replace the escaped characters in a EPC pure identity URI

    Args:
        uri (str): EPC pure identity URI

    Returns:
        str: Escaped URI string
    """
    return (
        uri.replace("%22", '"')
        .replace("%26", "&")
        .replace("%2F", "/")
        .replace("%3C", "<")
        .replace("%3E", ">")
        .replace("%3F", "?")
        .replace("%25", "%")
    )


def revert_uri_escapes(uri: str) -> str:
    """Revert the escaped character in a EPC pure identity URI

    Args:
        uri (str): EPC pure identity URI

    Returns:
        str: Reverted escaped characters URI
    """
    return (
        uri.replace("%", "%25")
        .replace('"', "%22")
        .replace("&", "%26")
        .replace("/", "%2F")
        .replace("<", "%3C")
        .replace(">", "%3E")
        .replace("?", "%3F")
    )


def int_to_binary(integer: int, num_bits: int) -> str:
    """Convert an integer to a certain length bit string

    Args:
        integer (int): Integer
        num_bits (int): Amount of bits in bit string

    Returns:
        str: Integer as bit string
    """
    return f"{integer:0{num_bits}b}"


def binary_to_int(binary: str) -> int:
    """Convert a binary string to an integer

    Args:
        binary (str): Binary string

    Returns:
        int: Integer value of binary string
    """
    return int(binary, 2)


def str_to_binary(string: str, num_bits: int) -> str:
    """Convert an integer as a string into a binary string of a given amount of bits.

    Args:
        string (str): String to convert
        num_bits (int): Amount of bits in bit string

    Returns:
        str: Integer string as bit string
    """
    return int_to_binary(int(string), num_bits)


def base64_to_hex(base64_string: str) -> str:
    """Convert base64 string to hexadecimal string

    Args:
        base64_string (str): Base64 string

    Returns:
        str: Hexadecimal representation
    """
    # Add padding to ensure valid padding
    return base64.b64decode(f"{base64_string}==").hex()


def hex_to_base64(hex_string: str) -> str:
    """Convert a hexadecimal string into base64 string

    Args:
        hex_string (str): Hexadecimal string

    Returns:
        str: Base64 encoded string
    """
    return base64.b64encode(bytes.fromhex(hex_string)).decode("utf-8")


def hex_to_binary(hex_string: str) -> str:
    """Convert hexadecimal string to binary

    Args:
        hex_string (str): Hexadecimal string

    Returns:
        str: Binary string
    """
    return f"{int(hex_string, 16):0{len(hex_string * 4)}b}"


def binary_to_hex(binary_string: str) -> str:
    """Convert binary string to hexadecimal string
    Resulting hex will be uppercase

    Args:
        binary_string (str): Binary string

    Returns:
        str: Hexadecimal string
    """
    return f"{int(binary_string, 2):x}".upper()


def encode_string(string: str, num_bits: int) -> str:
    """Encode a string into a bit string of a certain length

    Args:
        string (str): String to binary encode
        num_bits (int): Number of bits for resulting binary string

    Returns:
        str: Binary string
    """
    res = ""
    for g in re.split("(%[0-9a-fA-F]{2})", string):
        if len(g) == 0:
            continue
        elif g[0] != "%":
            res += "".join([str_to_binary(str(ord(s)), 7) for s in g])
        else:
            res += str_to_binary(str(int(g[1:], 16)), 7)
    return f"{res:<0{num_bits}}"


def decode_string_six_bits(binary: str, max_chars: int) -> str:
    """Decode binary string by decoding every sequence of six bits.

    Args:
        binary (str): Binary string
        max_chars (int): Maximum length of resulting string

    Raises:
        ConvertException: Resulting string too large

    Returns:
        str: Decoded string
    """
    res = ""
    for g in re.split("([0-1]{6})", binary):
        if g == "000000":
            break
        if len(g) < 6:
            continue
        elif g.startswith("10") or g.startswith("11"):
            res += chr(int(g, 2))
        else:
            res += chr(64 + int(g, 2))

    if len(res) > max_chars:
        raise ConvertException(message="Too many characters decoded!")

    return res.replace("#", "%23").replace("/", "%2F")


def encode_string_six_bits(string: str) -> str:
    """Encode a string by encoding every character into a six bit sequence.

    Args:
        string (str): String to encode

    Returns:
        str: Encoded string
    """
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
            res += str_to_binary(str(int(g[1:], 16)), 6)
    return f"{res}000000"


def decode_binary_char(binary: str) -> str:
    """Decode a single binary sequence of seven bits

    Args:
        binary (str): Binary sequence

    Returns:
        str: Decoded string
    """
    if binary == "0000000":
        return ""
    elif binary in ESCAPE_CHARACTERS:
        return ESCAPE_CHARACTERS[binary]
    else:
        return chr(int(binary, 2))


def decode_string(binary: str) -> str:
    """Decode a binary string per seven bits.

    Args:
        binary (str): Binary string to decode

    Returns:
        str: Decoded string
    """
    return "".join(
        list(
            map(
                decode_binary_char,
                re.findall("." * 7, binary),
            )
        )
    )


def encode_partition_table(
    parts: List[str],
    partition_table: Dict[int, Dict[str, int]],
    string_partition=False,
    six_bit_variable_partition=False,
) -> str:
    """Encode a string based on a partition table

    Args:
        parts (List[str]): Parts of the string to encode
        partition_table (List[Dict[str, Dict[str, int]]]): Partition table
        string_partition (bool, optional): Whether to use string partition table.
            Defaults to False.
        six_bit_variable_partition (bool, optional): Whether to use six bit variable partition table.
            Defaults to False.

    Returns:
        str: Encoded string
    """
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
        D_bin = (
            str_to_binary(D, partition["N"])
            if partition["K"] != 0
            else "0" * partition["N"]
        )

    return P_bin + C_bin + D_bin


def decode_partition_table(
    binary_string: str,
    partition_table: Dict[int, Dict[str, int]],
    unpadded_partition=False,
    string_partition=False,
    six_bit_variable_partition=False,
) -> str:
    """Decode a binary string using a partition table.

    Args:
        binary_string (str): Binary string to decode
        partition_table (List[Dict[str, Dict[str, int]]]): Partition table
        unpadded_partition (bool, optional): Whether to use unpadded partitioning. Defaults to False.
        string_partition (bool, optional): Whether to use string partitioning. Defaults to False.
        six_bit_variable_partition (bool, optional): Whether to use six bit variable partitioning. Defaults to False.

    Raises:
        ConvertException: Invalid partition header
        ConvertException: Too long company prefix
        ConvertException: Too long item reference

    Returns:
        str: Decoded string
    """
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
        D = str(binary_to_int(D_bin)) if partition["K"] != 0 else ""

    compare_D = not (
        unpadded_partition or string_partition or six_bit_variable_partition
    )

    if not C < pow(10, partition["L"]):
        raise ConvertException(message=f"Company prefix length too large")
    if D != "" and compare_D and not int(D) < pow(10, partition["K"]):
        raise ConvertException(message=f"Item reference length too large")

    return f"{C:>0{partition['L']}}.{D:>0{partition['K'] if compare_D else 0}}"


def encode_numeric_string(string: str, bit_count: int) -> str:
    """Encode a numeric string

    Args:
        string (str): String to encode
        bit_count (int): Number of bits for resulting string

    Raises:
        ConvertException: Character string invalid

    Returns:
        str: Encoded string
    """
    if 2 * pow(10, len(string)) >= pow(2, bit_count):
        raise ConvertException(message="Invalid character string")

    return str_to_binary(f"1{string}", bit_count)


def decode_numeric_string(binary: str) -> str:
    """Decode a numeric string

    Args:
        binary (str): Binary string

    Raises:
        ConvertException: Numeric string invalid

    Returns:
        str: Decoded numeric string
    """
    string = f"{int(binary, 2)}"

    if len(string) <= 1 or string[0] != "1":
        raise ConvertException(message="Invalid numeric string")

    return string[1:]


def encode_fixed_width_integer(string: str, bit_count: int) -> str:
    """Encode a string using fixed width integer

    Args:
        string (str): String to encode
        bit_count (int): Number of bits for resulting binary string

    Raises:
        ConvertException: Fixed width numeric integer too large

    Returns:
        str: Encoded fixed width integer string
    """
    if int(string) >= (pow(10, int(bit_count * log(2) / log(10))) - 1):
        raise ConvertException(message="Fixed width numeric integer too large")

    return str_to_binary(string, bit_count)


def decode_fixed_width_integer(binary: str) -> str:
    """Decode a fixed width integer binary string

    Args:
        binary (str): Binary string

    Raises:
        ConvertException: Bits cannot be converted into the required number of digits

    Returns:
        str: Decoded fixed width integer string
    """
    D = int(len(binary) * log(2) / log(10))
    if int(binary, 2) > pow(10, D) - 1:
        raise ConvertException(message=f"Bits cannot be converted to {D} digits")

    return f"{int(binary, 2):0>{D}}"


def decode_cage_code(binary: str) -> str:
    """Decode a string using cage codes

    Args:
        binary (str): Binary string to decode

    Returns:
        str: Decoded string
    """
    return "".join(
        [chr(int(g, 2)) if g != "" else "" for g in re.split("([0-1]{8})", binary)]
    ).replace(" ", "")


def encode_cage_code(chars: str) -> str:
    """Encode a string using cage codes

    Args:
        chars (str): Character sequence to encode

    Returns:
        str: Encoded string
    """
    return "".join([f"{ord(char):0>8b}" for char in chars])


def decode_cage_code_six_bits(binary: str) -> str:
    """Decode a string using six bit cage codes

    Args:
        binary (str): Binary string to decode

    Returns:
        str: Decoded string
    """
    if binary.startswith("100000"):
        binary = binary[6:]

    return decode_string_six_bits(binary, 6)


def encode_cage_code_six_bits(chars: str) -> str:
    """Encode a character sequence using six bit cage codes

    Args:
        chars (str): Character sequence to encode

    Returns:
        str: Encoded string
    """
    binary = f"{encode_string_six_bits(chars)[:-6]}"
    if len(binary) == 30:
        binary = "100000" + binary
    return binary


def verify_gs3a3_component(gs3a3_component: str):
    """Verify whether a given GS3A3 component is valid

    Args:
        gs3a3_component (str): GS3A3 component

    Raises:
        ConvertException: Component not valid
    """
    res = ""
    for g in re.split("(%\d\d)", gs3a3_component):
        if len(g) == 0:
            continue
        elif g[0] != "%":
            res += g
        else:
            res += chr(int(g[1:], 16))

    if not VERIFY_GS3A3_CHARS_REGEX.fullmatch(res):
        raise ConvertException()


def calculate_checksum(digits: str) -> int:
    """Calculate the checksum for GS1 element strings for a digit string

    Args:
        digits (str): String of digits

    Returns:
        int: Check digit
    """
    digit_list = [int(d) for d in digits]
    odd, even = digit_list[1::2], digit_list[0::2]

    if len(digits) % 2 == 0:
        val1 = sum(odd)
        val2 = sum(even)
    else:
        val1 = sum(even)
        val2 = sum(odd)

    checksum = (10 - ((3 * (val1) + (val2)) % 10)) % 10

    return checksum


def parse_header_and_truncate_binary(
    binary_string: str, header_to_schemes: Dict[str, Enum]
) -> Tuple[Enum, str]:
    """Parse a binary header, detect the scheme and truncate the binary string based on the scheme.

    Args:
        binary_string (str): Full length binary string
        header_to_schemes (Dict[str, str]): Mapping from binary headers to schemes

    Raises:
        ConvertException: Invalid binary header
        ConvertException: Binary string too short

    Returns:
        Tuple[Enum, str]: Scheme and truncated binary
    """
    header = binary_string[:8]

    try:
        scheme = header_to_schemes[header]
    except ValueError:
        raise ConvertException(message=f"{header} is not a valid header")

    _, size = scheme.value.split("-")
    size = int(size) if size.isnumeric() else None

    if size and size > len(binary_string):
        raise ConvertException(
            message=f"Invalid binary size, expected (>=): {size} actual: {len(binary_string)}"
        )

    truncated_binary = binary_string[:size]

    return scheme, truncated_binary
