import unittest

from epcpy.epc_schemes.upui import UPUI
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta, TestGS1ElementMeta


class TestUPUIInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=UPUI,
    valid_data=[
        {
            "name": "test_valid_upui_1",
            "uri": "urn:epc:id:upui:1234567.089456.51qIgY)%3C%26Jp3*j7'SDB",
        },
        {
            "name": "test_valid_upui_2",
            "uri": "urn:epc:id:upui:123456.0894567.51qIgY)%3C%26Jp3*j7'SDB",
        },
        {
            "name": "test_valid_upui_3",
            "uri": "urn:epc:id:upui:123456789012.0.51qIgY)%3C%26Jp3*j7'SDB",
        },
        {
            "name": "test_valid_upui_4",
            "uri": "urn:epc:id:upui:123456789012.0.0123456789012346578901234657",
        },
        {
            "name": "test_valid_upui_5",
            "uri": "urn:epc:id:upui:123456789012.0.0",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_upui_identifier",
            "uri": "urn:epc:id:upi:123456789012.0.0",
        },
        {
            "name": "test_invalid_upui_component1_1",
            "uri": "urn:epc:id:upui:12346.0894567.51qIgY)%3C%26Jp3*j7'SDB",
        },
        {
            "name": "test_invalid_upui_component1_2",
            "uri": "urn:epc:id:upui:1234567890123.0.51qIgY)%3C%26Jp3*j7'SDB",
        },
        {
            "name": "test_invalid_upui_serial_too_long",
            "uri": "urn:epc:id:upui:123456789012.0.01234567890123465789012346578",
        },
        {
            "name": "test_invalid_upui_invalid_chars",
            "uri": "urn:epc:id:upui:123456789012.0.012345678901234%23",
        },
    ],
):
    pass


class TestUPUIGS1Key(
    unittest.TestCase,
    metaclass=TestGS1ElementMeta,
    scheme=UPUI,
    valid_data=[
        {
            "name": "test_valid_upui_gs1_element_string_1",
            "uri": "urn:epc:id:upui:1234567.089456.51qIgY)%3C%26Jp3*j7'SDB",
            "gs1_element_string": "(01)01234567894560(235)51qIgY)<&Jp3*j7'SDB",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_upui_gs1_element_string_2",
            "uri": "urn:epc:id:upui:123456.0894567.51qIgY)%3C%26Jp3*j7'SDB",
            "gs1_element_string": "(01)01234568945674(235)51qIgY)<&Jp3*j7'SDB",
            "company_prefix_length": 6,
        },
        {
            "name": "test_valid_upui_gs1_element_string_3",
            "uri": "urn:epc:id:upui:123456789012.0.51qIgY)%3C%26Jp3*j7'SDB",
            "gs1_element_string": "(01)01234567890128(235)51qIgY)<&Jp3*j7'SDB",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_upui_gs1_element_string_4",
            "uri": "urn:epc:id:upui:123456789012.0.0123456789012346578901234657",
            "gs1_element_string": "(01)01234567890128(235)0123456789012346578901234657",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_upui_gs1_element_string_5",
            "uri": "urn:epc:id:upui:123456789012.0.0",
            "gs1_element_string": "(01)01234567890128(235)0",
            "company_prefix_length": 12,
        },
    ],
    invalid_data=[],
):
    pass
