import unittest

from epcpy.epc_schemes.cpi import CPI, CPIFilterValues
from epcpy.utils.common import BinaryCodingSchemes
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestTagEncodableMeta,
)


class TestCPIInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=CPI,
    valid_data=[
        {
            "name": "test_valid_cpi_1",
            "uri": "urn:epc:id:cpi:0614141.123ABC.123456789",
        },
        {
            "name": "test_valid_cpi_2",
            "uri": "urn:epc:id:cpi:0614141.12-456.123456789",
        },
        {
            "name": "test_valid_cpi_3",
            "uri": "urn:epc:id:cpi:0614141.1%231456.123456789",
        },
        {
            "name": "test_valid_cpi_4",
            "uri": "urn:epc:id:cpi:0614141.123456.0",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_cpi_identifier",
            "uri": "urn:epc:id:ci:0614141.123456.0",
        },
        {
            "name": "test_invalid_cpi_serial_starting_with_zero",
            "uri": "urn:epc:id:cpi:0614141.123456.01",
        },
        {
            "name": "test_invalid_cpi_percent23_wrong_location",
            "uri": "urn:epc:id:cpi:0614141.123456.2%232WMA52",
        },
        {
            "name": "test_invalid_cpi_percent23_wrong_location_2",
            "uri": "urn:epc:id:cpi:06%231141.123456.22252",
        },
        {
            "name": "test_invalid_cpi_invalid_company_pref",
            "uri": "urn:epc:id:cpi:0641411231321.1%231456.123456789",
        },
        {
            "name": "test_invalid_cpi_invalid_company_pref_2",
            "uri": "urn:epc:id:cpi:01234.1%231456.123456789",
        },
        {
            "name": "test_invalid_cpi_serial_too_long",
            "uri": "urn:epc:id:cpi:0614141.1%231456.1234567891231",
        },
    ],
):
    pass


class TestCPITagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=CPI,
    valid_data=[
        {
            "name": "test_valid_cpi_tag_encodable_1",
            "uri": "urn:epc:id:cpi:0614141.12-456.123456789",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_VAR,
                "filter_value": CPIFilterValues.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:cpi-var:0.0614141.12-456.123456789",
            "hex": "3D14257BF71CADD35D8000075BCD1500",
        },
        {
            "name": "test_valid_cpi_tag_encodable_2",
            "uri": "urn:epc:id:cpi:0614141.123456.0",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_96,
                "filter_value": CPIFilterValues.RESERVED_1,
            },
            "tag_uri": "urn:epc:tag:cpi-96:1.0614141.123456.0",
            "hex": "3C34257BF400F12000000000",
        },
        {
            "name": "test_valid_cpi_tag_encodable_3",
            "uri": "urn:epc:id:cpi:0614141.1234567890.0",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_VAR,
                "filter_value": CPIFilterValues.RESERVED_1,
            },
            "tag_uri": "urn:epc:tag:cpi-var:1.0614141.1234567890.0",
            "hex": "3D34257BF71CB3D35DB7E39C000000000000",
        },
        {
            "name": "test_valid_cpi_tag_encodable_4",
            "uri": "urn:epc:id:cpi:0614141.123467890.100000000000",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_VAR,
                "filter_value": CPIFilterValues.RESERVED_5,
            },
            "tag_uri": "urn:epc:tag:cpi-var:5.0614141.123467890.100000000000",
            "hex": "3DB4257BF71CB3D36DF8E70005D21DBA0000",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_cpi_tag_encodable_invalid_syntax",
            "uri": "urn:epc:id:cpi:0614141.12-456.123456789",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_96,
                "filter_value": CPIFilterValues.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_cpi_tag_encodable_invalid_part_length",
            "uri": "urn:epc:id:cpi:0614141.1234567890.0",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_96,
                "filter_value": CPIFilterValues.RESERVED_1,
            },
        },
        {
            "name": "test_invalid_cpi_tag_encodable_serial_out_of_range",
            "uri": "urn:epc:id:cpi:0614141.123467890.100000000000",
            "kwargs": {
                "binary_coding_scheme": BinaryCodingSchemes.CPI_96,
                "filter_value": CPIFilterValues.RESERVED_5,
            },
        },
    ],
):
    pass
