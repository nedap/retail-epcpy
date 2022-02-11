import unittest

from epcpy.epc_schemes.gsrn import GSRN, GSRNFilterValues
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestGSRNInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GSRN,
    valid_data=[
        {
            "name": "test_valid_gsrn_1",
            "uri": "urn:epc:id:gsrn:0614141.1234567890",
        },
        {
            "name": "test_valid_gsrn_2",
            "uri": "urn:epc:id:gsrn:012345678901.01234",
        },
        {
            "name": "test_valid_gsrn_3",
            "uri": "urn:epc:id:gsrn:000000.00000000000",
        },
        {
            "name": "test_valid_gsrn_4",
            "uri": "urn:epc:id:gsrn:000000000000.00000",
        },
        {
            "name": "test_valid_gsrn_5",
            "uri": "urn:epc:id:gsrn:999999999999.99999",
        },
        {
            "name": "test_valid_gsrn_6",
            "uri": "urn:epc:id:gsrn:999999.99999999999",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_gsrn_identifier",
            "uri": "urn:epc:id:gsrnp:0614141.1234567890",
        },
        {
            "name": "test_invalid_gsrn_invalid_company_pref_1",
            "uri": "urn:epc:id:gsrn:00000.000000000000",
        },
        {
            "name": "test_invalid_gsrn_invalid_company_pref_2",
            "uri": "urn:epc:id:gsrn:0000000000000.0000",
        },
        {
            "name": "test_invalid_gsrn_invalid_char_1",
            "uri": "urn:epc:id:gsrn:99A999.99999999999",
        },
        {
            "name": "test_invalid_gsrn_invalid_char_2",
            "uri": "urn:epc:id:gsrn:999999.9999999A999",
        },
        {
            "name": "test_invalid_gsrn_too_short",
            "uri": "urn:epc:id:gsrn:999999.9",
        },
        {
            "name": "test_invalid_gsrn_too_long",
            "uri": "urn:epc:id:gsrn:999999.999999999999",
        },
    ],
):
    pass


class TestGSRNGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=GSRN,
    valid_data=[
        {
            "name": "test_valid_gsrn_gs1_key_1",
            "uri": "urn:epc:id:gsrn:0614141.1234567890",
            "gs1_key": "061414112345678902",
        },
        {
            "name": "test_valid_gsrn_gs1_key_2",
            "uri": "urn:epc:id:gsrn:012345678901.01234",
            "gs1_key": "012345678901012342",
        },
        {
            "name": "test_valid_gsrn_gs1_key_3",
            "uri": "urn:epc:id:gsrn:000000.00000000000",
            "gs1_key": "000000000000000000",
        },
        {
            "name": "test_valid_gsrn_gs1_key_4",
            "uri": "urn:epc:id:gsrn:000000000000.00000",
            "gs1_key": "000000000000000000",
        },
        {
            "name": "test_valid_gsrn_gs1_key_5",
            "uri": "urn:epc:id:gsrn:999999999999.99999",
            "gs1_key": "999999999999999995",
        },
        {
            "name": "test_valid_gsrn_gs1_key_6",
            "uri": "urn:epc:id:gsrn:999999.99999999999",
            "gs1_key": "999999999999999995",
        },
    ],
    invalid_data=[],
):
    pass


class TestGSRNTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=GSRN,
    valid_data=[
        {
            "name": "test_valid_gsrn_tag_encodable_1",
            "uri": "urn:epc:id:gsrn:0614141.1234567890",
            "kwargs": {"filter_value": GSRNFilterValues.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrn-96:0.0614141.1234567890",
            "hex": "2D14257BF4499602D2000000",
        },
        {
            "name": "test_valid_gsrn_tag_encodable_2",
            "uri": "urn:epc:id:gsrn:012345678901.01234",
            "kwargs": {"filter_value": GSRNFilterValues.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrn-96:0.012345678901.01234",
            "hex": "2D000B7F7070D404D2000000",
        },
        {
            "name": "test_valid_gsrn_tag_encodable_3",
            "uri": "urn:epc:id:gsrn:000000.00000000000",
            "kwargs": {"filter_value": GSRNFilterValues.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrn-96:0.000000.00000000000",
            "hex": "2D1800000000000000000000",
        },
        {
            "name": "test_valid_gsrn_tag_encodable_4",
            "uri": "urn:epc:id:gsrn:000000000000.00000",
            "kwargs": {"filter_value": GSRNFilterValues.RESERVED_5},
            "tag_uri": "urn:epc:tag:gsrn-96:5.000000000000.00000",
            "hex": "2DA000000000000000000000",
        },
        {
            "name": "test_valid_gsrn_tag_encodable_5",
            "uri": "urn:epc:id:gsrn:999999999999.99999",
            "kwargs": {"filter_value": GSRNFilterValues.RESERVED_5},
            "tag_uri": "urn:epc:tag:gsrn-96:5.999999999999.99999",
            "hex": "2DA3A352943FFD869F000000",
        },
        {
            "name": "test_valid_gsrn_tag_encodable_6",
            "uri": "urn:epc:id:gsrn:999999.99999999999",
            "kwargs": {"filter_value": GSRNFilterValues.ALL_OTHERS},
            "tag_uri": "urn:epc:tag:gsrn-96:0.999999.99999999999",
            "hex": "2D1BD08FD74876E7FF000000",
        },
    ],
    invalid_data=[],
):
    pass
