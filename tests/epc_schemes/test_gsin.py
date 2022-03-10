import unittest

from epcpy.epc_schemes.gsin import GSIN
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta, TestGS1KeyedMeta


class TestGSINInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GSIN,
    valid_data=[
        {
            "name": "test_valid_gsin_1",
            "uri": "urn:epc:id:gsin:0614141.123456789",
        },
        {
            "name": "test_valid_gsin_2",
            "uri": "urn:epc:id:gsin:061414112345.0123",
        },
        {
            "name": "test_valid_gsin_3",
            "uri": "urn:epc:id:gsin:061414.0123456789",
        },
        {
            "name": "test_valid_gsin_4",
            "uri": "urn:epc:id:gsin:061414.0000000000",
        },
        {
            "name": "test_valid_gsin_5",
            "uri": "urn:epc:id:gsin:000000.0000000000",
        },
        {
            "name": "test_valid_gsin_6",
            "uri": "urn:epc:id:gsin:999999999999.9999",
        },
        {
            "name": "test_valid_gsin_7",
            "uri": "urn:epc:id:gsin:999999.9999999999",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_gsin_identifier",
            "uri": "urn:epc:id:gsn:999999.9999999999",
        },
        {
            "name": "test_invalid_gsin_company_prefix_1",
            "uri": "urn:epc:id:gsin:9999999999999.999",
        },
        {
            "name": "test_invalid_gsin_company_prefix_2",
            "uri": "urn:epc:id:gsin:99999.99999999999",
        },
        {
            "name": "test_invalid_gsin_incorrect_digit_amount_1",
            "uri": "urn:epc:id:gsin:0123456789:0123456",
        },
        {
            "name": "test_invalid_gsin_incorrect_digit_amount_2",
            "uri": "urn:epc:id:gsin:0123456789:01234",
        },
        {
            "name": "test_invalid_gsin_invalid_chars",
            "uri": "urn:epc:id:gsin:0123456789:0123A4",
        },
    ],
):
    pass


class TestGSINGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=GSIN,
    valid_data=[
        {
            "name": "test_valid_gsin_gs1_key_1",
            "uri": "urn:epc:id:gsin:0614141.123456789",
            "gs1_key": "06141411234567890",
            "gs1_element_string": "(402)06141411234567890",
        },
        {
            "name": "test_valid_gsin_gs1_key_2",
            "uri": "urn:epc:id:gsin:061414112345.0123",
            "gs1_key": "06141411234501238",
            "gs1_element_string": "(402)06141411234501238",
        },
        {
            "name": "test_valid_gsin_gs1_key_3",
            "uri": "urn:epc:id:gsin:061414.0123456789",
            "gs1_key": "06141401234567891",
            "gs1_element_string": "(402)06141401234567891",
        },
        {
            "name": "test_valid_gsin_gs1_key_4",
            "uri": "urn:epc:id:gsin:061414.0000000000",
            "gs1_key": "06141400000000006",
            "gs1_element_string": "(402)06141400000000006",
        },
        {
            "name": "test_valid_gsin_gs1_key_5",
            "uri": "urn:epc:id:gsin:000000.0000000000",
            "gs1_key": "00000000000000000",
            "gs1_element_string": "(402)00000000000000000",
        },
        {
            "name": "test_valid_gsin_gs1_key_6",
            "uri": "urn:epc:id:gsin:999999999999.9999",
            "gs1_key": "99999999999999992",
            "gs1_element_string": "(402)99999999999999992",
        },
        {
            "name": "test_valid_gsin_gs1_key_7",
            "uri": "urn:epc:id:gsin:999999.9999999999",
            "gs1_key": "99999999999999992",
            "gs1_element_string": "(402)99999999999999992",
        },
    ],
    invalid_data=[],
):
    pass
