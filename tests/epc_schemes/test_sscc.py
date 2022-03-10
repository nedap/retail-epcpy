import unittest

from epcpy.epc_schemes.sscc import SSCC, SSCCFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestSSCCInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=SSCC,
    valid_data=[
        {
            "name": "test_valid_sscc_1",
            "uri": "urn:epc:id:sscc:0614141.1234567890",
        },
        {
            "name": "test_valid_sscc_2",
            "uri": "urn:epc:id:sscc:061414.12345678901",
        },
        {
            "name": "test_valid_sscc_3",
            "uri": "urn:epc:id:sscc:061414123456.12345",
        },
        {
            "name": "test_valid_sscc_4",
            "uri": "urn:epc:id:sscc:061414123456.00000",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sscc_identifier",
            "uri": "urn:epc:id:ssc:0614141.1234567890",
        },
        {
            "name": "test_invalid_sscc_company_prefix_1",
            "uri": "urn:epc:id:sscc:06141.112345678901",
        },
        {
            "name": "test_invalid_sscc_company_prefix_2",
            "uri": "urn:epc:id:sscc:0614141234567.2345",
        },
    ],
):
    pass


class TestSSCCGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=SSCC,
    valid_data=[
        {
            "name": "test_valid_sscc_gs1_key_1",
            "uri": "urn:epc:id:sscc:0614141.1234567890",
            "gs1_key": "106141412345678908",
            "gs1_element_string": "(00)106141412345678908",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_sscc_gs1_key_2",
            "uri": "urn:epc:id:sscc:061414.12345678901",
            "gs1_key": "106141423456789018",
            "gs1_element_string": "(00)106141423456789018",
            "company_prefix_length": 6,
        },
        {
            "name": "test_valid_sscc_gs1_key_3",
            "uri": "urn:epc:id:sscc:061414123456.12345",
            "gs1_key": "106141412345623458",
            "gs1_element_string": "(00)106141412345623458",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_sscc_gs1_key_4",
            "uri": "urn:epc:id:sscc:061414123456.00000",
            "gs1_key": "006141412345600001",
            "gs1_element_string": "(00)006141412345600001",
            "company_prefix_length": 12,
        },
    ],
    invalid_data=[],
):
    pass


class TestSSCCTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=SSCC,
    valid_data=[
        {
            "name": "test_valid_sscc_tag_encodable_1",
            "uri": "urn:epc:id:sscc:0614141.1234567890",
            "kwargs": {
                "filter_value": SSCCFilterValue.FULL_CASE,
            },
            "tag_uri": "urn:epc:tag:sscc-96:2.0614141.1234567890",
            "hex": "3154257BF4499602D2000000",
        },
        {
            "name": "test_valid_sscc_tag_encodable_2",
            "uri": "urn:epc:id:sscc:061414.12345678901",
            "kwargs": {
                "filter_value": SSCCFilterValue.FULL_CASE,
            },
            "tag_uri": "urn:epc:tag:sscc-96:2.061414.12345678901",
            "hex": "31583BF982DFDC1C35000000",
        },
        {
            "name": "test_valid_sscc_tag_encodable_3",
            "uri": "urn:epc:id:sscc:061414123456.12345",
            "kwargs": {
                "filter_value": SSCCFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sscc-96:0.061414123456.12345",
            "hex": "31003932449F003039000000",
        },
        {
            "name": "test_valid_sscc_tag_encodable_4",
            "uri": "urn:epc:id:sscc:061414123456.00000",
            "kwargs": {
                "filter_value": SSCCFilterValue.RESERVED_5,
            },
            "tag_uri": "urn:epc:tag:sscc-96:5.061414123456.00000",
            "hex": "31A03932449F000000000000",
        },
    ],
    invalid_data=[],
):
    pass
