import unittest

from epcpy.epc_schemes.upui import UPUI
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta


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
