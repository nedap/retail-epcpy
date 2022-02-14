import unittest

from epcpy.epc_schemes.sgcn import SGCN, SGCNFilterValues
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestSGCNInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=SGCN,
    valid_data=[
        {
            "name": "test_valid_sgcn_1",
            "uri": "urn:epc:id:sgcn:4012345.67890.04711",
        },
        {
            "name": "test_valid_sgcn_2",
            "uri": "urn:epc:id:sgcn:4012345.67890.0",
        },
        {
            "name": "test_valid_sgcn_3",
            "uri": "urn:epc:id:sgcn:4012345.67890.01",
        },
        {
            "name": "test_valid_sgcn_4",
            "uri": "urn:epc:id:sgcn:401234512345..1",
        },
        {
            "name": "test_valid_sgcn_5",
            "uri": "urn:epc:id:sgcn:401231.123465.999999999999",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sgcn_identifier",
            "uri": "urn:epc:id:scn:4012345.67890.04711",
        },
        {
            "name": "test_invalid_sgcn_company_prefix_1",
            "uri": "urn:epc:id:sgcn:4012345123451..1",
        },
        {
            "name": "test_invalid_sgcn_company_prefix_2",
            "uri": "urn:epc:id:sgcn:40123.1123465.999999999999",
        },
        {
            "name": "test_invalid_sgcn_serial_too_long",
            "uri": "urn:epc:id:sgcn:401231.123465.9999999999999",
        },
        {
            "name": "test_invalid_sgcn_serial_too_short",
            "uri": "urn:epc:id:sgcn:401231.123465.",
        },
        {
            "name": "test_invalid_sgcn_illegal_chars",
            "uri": "urn:epc:id:sgcn:401231.123465.999ABCD999999",
        },
    ],
):
    pass


class TestSGCNGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=SGCN,
    valid_data=[
        {
            "name": "test_valid_sgcn_gs1_key_1",
            "uri": "urn:epc:id:sgcn:4012345.67890.04711",
            "gs1_key": "401234567890104711",
        },
        {
            "name": "test_valid_sgcn_gs1_key_2",
            "uri": "urn:epc:id:sgcn:4012345.67890.0",
            "gs1_key": "40123456789010",
        },
        {
            "name": "test_valid_sgcn_gs1_key_3",
            "uri": "urn:epc:id:sgcn:4012345.67890.01",
            "gs1_key": "401234567890101",
        },
        {
            "name": "test_valid_sgcn_gs1_key_4",
            "uri": "urn:epc:id:sgcn:401234512345..1",
            "gs1_key": "40123451234561",
        },
        {
            "name": "test_valid_sgcn_gs1_key_5",
            "uri": "urn:epc:id:sgcn:401231.123465.999999999999",
            "gs1_key": "4012311234650999999999999",
        },
    ],
    invalid_data=[],
):
    pass


class TestSGCNTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=SGCN,
    valid_data=[
        {
            "name": "test_valid_sgcn_tag_encodable_1",
            "uri": "urn:epc:id:sgcn:4012345.67890.04711",
            "kwargs": {
                "filter_value": SGCNFilterValues.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgcn-96:0.4012345.67890.04711",
            "hex": "3F14F4E4E612640000019907",
        },
        {
            "name": "test_valid_sgcn_tag_encodable_2",
            "uri": "urn:epc:id:sgcn:4012345.67890.0",
            "kwargs": {
                "filter_value": SGCNFilterValues.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgcn-96:0.4012345.67890.0",
            "hex": "3F14F4E4E61264000000000A",
        },
        {
            "name": "test_valid_sgcn_tag_encodable_3",
            "uri": "urn:epc:id:sgcn:4012345.67890.01",
            "kwargs": {
                "filter_value": SGCNFilterValues.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgcn-96:0.4012345.67890.01",
            "hex": "3F14F4E4E612640000000065",
        },
        {
            "name": "test_valid_sgcn_tag_encodable_4",
            "uri": "urn:epc:id:sgcn:401234512345..1",
            "kwargs": {
                "filter_value": SGCNFilterValues.RESERVED_7,
            },
            "tag_uri": "urn:epc:tag:sgcn-96:7.401234512345..1",
            "hex": "3FE175ADC32764000000000B",
        },
        {
            "name": "test_valid_sgcn_tag_encodable_5",
            "uri": "urn:epc:id:sgcn:401231.123465.999999999999",
            "kwargs": {
                "filter_value": SGCNFilterValues.RESERVED_7,
            },
            "tag_uri": "urn:epc:tag:sgcn-96:7.401231.123465.999999999999",
            "hex": "3FF987D3C3C493D1A94A1FFF",
        },
    ],
    invalid_data=[],
):
    pass
