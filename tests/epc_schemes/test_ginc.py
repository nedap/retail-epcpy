import unittest

from epcpy.epc_schemes.ginc import GINC
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta, TestGS1KeyedMeta


class TestGINCInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GINC,
    valid_data=[
        {
            "name": "test_valid_ginc_1",
            "uri": "urn:epc:id:ginc:0614141.xyz3311cba",
        },
        {
            "name": "test_valid_ginc_2",
            "uri": "urn:epc:id:ginc:0614141.0",
        },
        {
            "name": "test_valid_ginc_3",
            "uri": "urn:epc:id:ginc:0614141.01",
        },
        {
            "name": "test_valid_ginc_4",
            "uri": "urn:epc:id:ginc:061411.01ABc%2FD",
        },
        {
            "name": "test_valid_ginc_5",
            "uri": "urn:epc:id:ginc:012345.012345678901234567890123",
        },
        {
            "name": "test_valid_ginc_6",
            "uri": "urn:epc:id:ginc:012345678901.012345678901234567",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_ginc_identifier",
            "uri": "urn:epc:id:gnc:061411.01ABc%2FD",
        },
        {
            "name": "test_invalid_ginc_company_prefix_1",
            "uri": "urn:epc:id:ginc:06141.01ABc%2FD",
        },
        {
            "name": "test_invalid_ginc_company_prefix_2",
            "uri": "urn:epc:id:ginc:0614117890123.01ABc%2FD",
        },
        {
            "name": "test_invalid_ginc_serial_too_long_1",
            "uri": "urn:epc:id:ginc:012345.0123456789012345678901234",
        },
        {
            "name": "test_invalid_ginc_serial_too_long_1",
            "uri": "urn:epc:id:ginc:012345.0123456789012345678901234",
        },
        {
            "name": "test_invalid_ginc_serial_too_long_2",
            "uri": "urn:epc:id:ginc:012345678901.0123456789012345678",
        },
    ],
):
    pass


class TestGINCGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=GINC,
    valid_data=[
        {
            "name": "test_valid_ginc_gs1_key_1",
            "uri": "urn:epc:id:ginc:0614141.xyz3311cba",
            "gs1_key": "0614141xyz3311cba",
            "gs1_element_string": "(401)0614141xyz3311cba"
        },
        {
            "name": "test_valid_ginc_gs1_key_2",
            "uri": "urn:epc:id:ginc:0614141.0",
            "gs1_key": "06141410",
            "gs1_element_string": "(401)06141410"
        },
        {
            "name": "test_valid_ginc_gs1_key_3",
            "uri": "urn:epc:id:ginc:0614141.01",
            "gs1_key": "061414101",
            "gs1_element_string": "(401)061414101"
        },
        {
            "name": "test_valid_ginc_gs1_key_4",
            "uri": "urn:epc:id:ginc:061411.01ABc%2FD",
            "gs1_key": "06141101ABc/D",
            "gs1_element_string": "(401)06141101ABc/D"
        },
        {
            "name": "test_valid_ginc_gs1_key_5",
            "uri": "urn:epc:id:ginc:012345.012345678901234567890123",
            "gs1_key": "012345012345678901234567890123",
            "gs1_element_string": "(401)012345012345678901234567890123"
        },
        {
            "name": "test_valid_ginc_gs1_key_6",
            "uri": "urn:epc:id:ginc:012345678901.012345678901234567",
            "gs1_key": "012345678901012345678901234567",
            "gs1_element_string": "(401)012345678901012345678901234567"
        },
    ],
    invalid_data=[],
):
    pass
