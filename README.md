# EPCPY
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/epcpy.svg)](https://badge.fury.io/py/epcpy)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/epcpy.svg)](https://pypi.org/project/epcpy/)


A Python module for creation, validation, and transformation of EPC representations as defined in GS1's EPC Tag Data Standard (https://www.gs1.org/standards/rfid/tds).

**Table of contents**
- [EPCPY](#epcpy)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Scheme types](#scheme-types)
  - [Available schemes](#available-schemes)
  - [Generic parsers](#generic-parsers)
  - [Example usage](#example-usage)
    - [SGTIN](#sgtin)
      - [Pure identity](#pure-identity)
      - [GS1Keyed](#gs1keyed)
      - [Tag encoded](#tag-encoded)
    - [Generic parsing](#generic-parsing)
  - [Exceptions](#exceptions)
  - [Development](#development)
    - [Testing](#testing)
    - [Coverage](#coverage)
    - [Notebook](#notebook)

## Requirements
- Python >= 3.7

## Installation
```
pip install epcpy
```
## Scheme types
Every scheme is an instance of the `EPCScheme` class, which allows scheme initialization using a constructor which accepts a EPC pure identity such as `urn:epc:id:sgtin:00000950.01093.Serial` or using the class method `from_epc_uri`. Aside from this base class, schemes can also be instances of the `GS1Keyed`, `GS1Element` and/or `TagEncodable` classes. These provide the following methods:

**EPCScheme**
- *constructor*
- `from_epc_uri`

**GS1Element / GS1Keyed**
- `from_gs1_element_string`
- `gs1_element_string`
- `gs1_key` (if `GS1Keyed`)

**TagEncodable**
- `from_binary`
- `from_hex`
- `from_base64`
- `from_tag_uri`
- `binary`
- `hex`
- `base64`
- `tag_uri`

An example highlighting the different options for the `SGTIN` scheme can be found [later in this document](#example-usage) .

## Available schemes
| **Scheme** |  **GS1 element**   |   **GS1 keyed**    | **Tag encodable**  |
| ---------- | :----------------: | :----------------: | :----------------: |
| ADI        |                    |                    | :heavy_check_mark: |
| BIC        |                    |                    |                    |
| CPI        | :heavy_check_mark: |                    | :heavy_check_mark: |
| GDTI       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| GIAI       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| GID        |                    |                    | :heavy_check_mark: |
| GINC       | :heavy_check_mark: | :heavy_check_mark: |                    |
| GRAI       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| GSIN       | :heavy_check_mark: | :heavy_check_mark: |                    |
| GSRN       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| GSRNP      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| IMOVN      |                    |                    |                    |
| ITIP       | :heavy_check_mark: |                    | :heavy_check_mark: |
| LGTIN      | :heavy_check_mark: | :heavy_check_mark: |                    |
| PGLN       | :heavy_check_mark: | :heavy_check_mark: |                    |
| SGCN       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SGLN       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SGTIN      | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| SSCC       | :heavy_check_mark: | :heavy_check_mark: | :heavy_check_mark: |
| UPUI       | :heavy_check_mark: |                    |                    |
| USDOD      |                    |                    | :heavy_check_mark: |

## Generic parsers
The following generic parser functions are available
- `base64_to_tag_encodable`
- `binary_to_tag_encodable`
- `hex_to_tag_encodable`
- `tag_uri_to_tag_encodable`
- `epc_pure_identity_to_gs1_element`
- `epc_pure_identity_to_gs1_element_string`
- `epc_pure_identity_to_gs1_key`
- `epc_pure_identity_to_gs1_keyed`
- `epc_pure_identity_to_scheme`
- `epc_pure_identity_to_tag_encodable`
- `get_gs1_key`

## Example usage
### SGTIN
#### Pure identity
Given an `SGTIN` in EPC URI representation, `urn:epc:id:sgtin:00000950.01093.Serial`, an epcpy `SGTIN` object can be created as follows
```python
from epcpy.epc_schemes import SGTIN

sgtin = SGTIN.from_epc_uri("urn:epc:id:sgtin:00000950.01093.Serial")

# Alternatively
sgtin = SGTIN("urn:epc:id:sgtin:00000950.01093.Serial")

sgtin.epc_uri
# urn:epc:id:sgtin:00000950.01093.Serial
```


#### GS1Keyed
Since `SGTIN` is `GS1Keyed`, several elements can be derived using
```python
sgtin.gs1_element_string()
# (01)00000095010939(21)Serial

sgtin.gs1_key()
# 00000095010939

from epcpy.epc_schemes.sgtin import GTIN_TYPE
sgtin.gs1_key(gtin_type=GTIN_TYPE.GTIN8) # GTIN14 is the default
# 95010939
```
Additionaly, an `SGTIN` can also be constructed from a GS1 element string if a company prefix length is provided
```python
SGTIN.from_gs1_element_string("(01)00000095010939(21)Serial", company_prefix_length=8)
```

#### Tag encoded
With some additional information an `SGTIN` can be encoded into a tag, subsequently the tag can for example be represented as tag uri, hexadecimal, base64 or binary string
```python
sgtin.tag_uri(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM)
# urn:epc:tag:sgtin-198:1.00000950.01093.Serial

sgtin.hex(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM)
# 36300001DB011169E5E5A70EC000000000000000000000000000


sgtin.base64(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM)
# NjAAAdsBEWnl5acOwAAAAAAAAAAAAAAAAAA

sgtin.binary(binary_coding_scheme=SGTIN.BinaryCodingScheme.SGTIN_198, filter_value=SGTINFilterValue.POS_ITEM)
# 001101100011000000000000000000...
```

Similary, given a `SGTIN` tag in hex `36300001DB011169E5E5A70EC000000000000000000000000000`, an `SGTIN` can be constructed
```python
SGTIN.from_hex("36300001DB011169E5E5A70EC000000000000000000000000000")

# from_binary, from_base64 and from_tag_uri are available as well
```

### Generic parsing
When dealing with arbitrary tags epcpy also provides generic parsing options.
```python
from epcpy import hex_to_epc

hex_to_epc("36300001DB011169E5E5A70EC000000000000000000000000000")
```
The following parsers are available:
- `base64_to_tag_encodable`
- `binary_to_tag_encodable`
- `epc_pure_identity_to_gs1_element`
- `epc_pure_identity_to_gs1_element_string`
- `epc_pure_identity_to_gs1_key`
- `epc_pure_identity_to_gs1_keyed`
- `epc_pure_identity_to_scheme`
- `epc_pure_identity_to_tag_encodable`
- `hex_to_tag_encodable`
- `tag_uri_to_tag_encodable`

Alternatively, the `get_gs1_key` method can be used to distill the GS1 key from a given string.
```python
from epcpy import get_gs1_key

get_gs1_key("36300001DB011169E5E5A70EC000000000000000000000000000")
# 00000095010939

get_gs1_key("urn:epc:tag:sgtin-198:1.00000950.01093.Serial")
# 00000095010939

get_gs1_key("urn:epc:idpat:sgtin:00000950.01093.*")
# 00000095010939
```
`get_gs1_key` is able to parse the following sources:
- EPC pure identity URIs
- EPC tag URIs
- GS1 element strings (company_prefix_length should be provided)
- EPC id pattern URIs
- Binary strings
- Hexadecimal strings

## Exceptions
Especially when applying generic parsing, exceptions may be thrown when passing invalid data. One can import the `ConvertException` class to specially deal with exceptions thrown by this library:
```python
from epcpy import ConvertException, get_gs1_key

try:
  get_gs1_key("urn:epc:idpat:sgtin:00000950.*.*")
except ConvertException as e:
  print(e)
  # Could not create valid scheme from given id pat
```

## Development

This project uses [Poetry](https://python-poetry.org/) for project management.
Poetry must be installed and available in `$PATH`.
After cloning run `poetry install` to install (development) dependencies.

### Testing
This module uses the Python unittest library. Run `poetry run test` for running the tests.

### Coverage
Run `poetry run coverage run -m unittest discover` to execute all tests with coverage. The resulting coverage can be reported using `poetry run coverage report --omit="*/test*"` for a textual view the terminal and with `poetry run coverage html --omit="*/test*"` for a webpage.

### Notebook
There is a sample notebook included in this repository, which can be used to quickly get a hands-on experience with the repository. The notebook might not be completely up-to-date and requires the `jupyter` package to run, which can be installed using `pip install jupyter`.