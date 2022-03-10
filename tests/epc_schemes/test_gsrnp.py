import unittest

from epcpy.epc_schemes.gsrnp import GSRNP, GSRNPFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestGSRNPInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GSRNP,
    valid_data=[
        {
            "name": "test_valid_gsrnp_1",
            "uri": "urn:epc:id:gsrnp:0614141.1234567890",
        },
        {
            "name": "test_valid_gsrnp_2",
            "uri": "urn:epc:id:gsrnp:012345678901.01234",
        },
        {
            "name": "test_valid_gsrnp_3",
            "uri": "urn:epc:id:gsrnp:000000.00000000000",
        },
        {
            "name": "test_valid_gsrnp_4",
            "uri": "urn:epc:id:gsrnp:000000000000.00000",
        },
        {
            "name": "test_valid_gsrnp_5",
            "uri": "urn:epc:id:gsrnp:999999999999.99999",
        },
        {
            "name": "test_valid_gsrnp_6",
            "uri": "urn:epc:id:gsrnp:999999.99999999999",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_gsrnp_identifier",
            "uri": "urn:epc:id:gsrnpp:0614141.1234567890",
        },
        {
            "name": "test_invalid_gsrnp_invalid_company_pref_1",
            "uri": "urn:epc:id:gsrnp:00000.000000000000",
        },
        {
            "name": "test_invalid_gsrnp_invalid_company_pref_2",
            "uri": "urn:epc:id:gsrnp:0000000000000.0000",
        },
        {
            "name": "test_invalid_gsrnp_invalid_char_1",
            "uri": "urn:epc:id:gsrnp:99A999.99999999999",
        },
        {
            "name": "test_invalid_gsrnp_invalid_char_2",
            "uri": "urn:epc:id:gsrnp:999999.9999999A999",
        },
        {
            "name": "test_invalid_gsrnp_too_short",
            "uri": "urn:epc:id:gsrnp:999999.9",
        },
        {
            "name": "test_invalid_gsrnp_too_long",
            "uri": "urn:epc:id:gsrnp:999999.999999999999",
        },
    ],
):
    pass


class TestGSRNPGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=GSRNP,
    valid_data=[
        {
            "name": "test_valid_gsrnp_gs1_key_1",
            "uri": "urn:epc:id:gsrnp:0614141.1234567890",
            "gs1_key": "061414112345678902",
            "gs1_element_string": "(8017)061414112345678902",
            "args": [7],
        },
        {
            "name": "test_valid_gsrnp_gs1_key_2",
            "uri": "urn:epc:id:gsrnp:012345678901.01234",
            "gs1_key": "012345678901012342",
            "gs1_element_string": "(8017)012345678901012342",
            "args": [12],
        },
        {
            "name": "test_valid_gsrnp_gs1_key_3",
            "uri": "urn:epc:id:gsrnp:000000.00000000000",
            "gs1_key": "000000000000000000",
            "gs1_element_string": "(8017)000000000000000000",
            "args": [6],
        },
        {
            "name": "test_valid_gsrnp_gs1_key_4",
            "uri": "urn:epc:id:gsrnp:000000000000.00000",
            "gs1_key": "000000000000000000",
            "gs1_element_string": "(8017)000000000000000000",
            "args": [12],
        },
        {
            "name": "test_valid_gsrnp_gs1_key_5",
            "uri": "urn:epc:id:gsrnp:999999999999.99999",
            "gs1_key": "999999999999999995",
            "gs1_element_string": "(8017)999999999999999995",
            "args": [12],
        },
        {
            "name": "test_valid_gsrnp_gs1_key_6",
            "uri": "urn:epc:id:gsrnp:999999.99999999999",
            "gs1_key": "999999999999999995",
            "gs1_element_string": "(8017)999999999999999995",
            "args": [6],
        },
    ],
    invalid_data=[],
):
    pass


class TestGSRNPTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=GSRNP,
    valid_data=[
        {
            "name": "test_valid_gsrnp_tag_encodable_1",
            "uri": "urn:epc:id:gsrnp:0614141.1234567890",
            "kwargs": {"filter_value": GSRNPFilterValue.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrnp-96:0.0614141.1234567890",
            "hex": "2E14257BF4499602D2000000",
        },
        {
            "name": "test_valid_gsrnp_tag_encodable_2",
            "uri": "urn:epc:id:gsrnp:012345678901.01234",
            "kwargs": {"filter_value": GSRNPFilterValue.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrnp-96:0.012345678901.01234",
            "hex": "2E000B7F7070D404D2000000",
        },
        {
            "name": "test_valid_gsrnp_tag_encodable_3",
            "uri": "urn:epc:id:gsrnp:000000.00000000000",
            "kwargs": {"filter_value": GSRNPFilterValue.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrnp-96:0.000000.00000000000",
            "hex": "2E1800000000000000000000",
        },
        {
            "name": "test_valid_gsrnp_tag_encodable_4",
            "uri": "urn:epc:id:gsrnp:000000000000.00000",
            "kwargs": {"filter_value": GSRNPFilterValue.RESERVED_5},
            "tag_uri": "urn:epc:tag:gsrnp-96:5.000000000000.00000",
            "hex": "2EA000000000000000000000",
        },
        {
            "name": "test_valid_gsrnp_tag_encodable_5",
            "uri": "urn:epc:id:gsrnp:999999999999.99999",
            "kwargs": {"filter_value": GSRNPFilterValue.RESERVED_5},
            "tag_uri": "urn:epc:tag:gsrnp-96:5.999999999999.99999",
            "hex": "2EA3A352943FFD869F000000",
        },
        {
            "name": "test_valid_gsrnp_tag_encodable_6",
            "uri": "urn:epc:id:gsrnp:999999.99999999999",
            "kwargs": {"filter_value": GSRNPFilterValue.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrnp-96:0.999999.99999999999",
            "hex": "2E1BD08FD74876E7FF000000",
        },
    ],
    invalid_data=[],
):
    pass
