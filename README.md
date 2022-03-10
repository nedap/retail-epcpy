# EPCPY
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

A Python module for creation, validation, and transformation of EPC representations as defined in GS1's EPC Tag Data Standard (https://www.gs1.org/standards/rfid/tds).

## Example usage

### SGTIN

#### Pure identity
Given an SGTIN in epc uri representation `urn:epc:id:sgtin:00000950.01093.Serial` an epcpy SGTIN object can be created as follows
```python
from epcpy.epc_schemes.sgtin import SGTIN

sgtin = SGTIN.from_epc_uri("urn:epc:id:sgtin:00000950.01093.Serial")
```
subsequently several elements can be derived using
```python
print(sgtin.gs1_element_string())
print(sgtin.gs1_key())
print(sgtin.gs1_key(gtin_type=GTIN_TYPE.GTIN14))
```

#### Tag encoded
With some additional information an SGTIN can be encoded into a tag, subsequently the tag can for example be represented as tag uri, hexadecimal binary or binary string
```python
print(sgtin.tag_uri(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM))
print(sgtin.hex(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM))
print(sgtin.binary(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM))
```
Similary, given a sgtin tag in hex `36300001DB011169E5E5A70EC000000000000000000000000000`, an SGTIN can be constructed
```python
SGTIN.from_hex("36300001DB011169E5E5A70EC000000000000000000000000000")
```

### Generic parsing
When dealing with arbitrary tags epcpy also provides generic parsing options
```python
from epcpy.utils.parsers import hex_to_epc

hex_to_epc("36300001DB011169E5E5A70EC000000000000000000000000000")
```

## Development
### Testing
This module uses the Python unittest library. Run `python -m unittest discover` for running the tests.

### Coverage
Make sure the `coverage` package is installed using `pip install coverage`. Next run `coverage run -m unittest discover` to execute all tests with coverage. The resulting coverage can be reported using `coverage report` in the terminal and with `coverage html` for a webpage.
