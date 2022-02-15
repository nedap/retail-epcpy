import unittest

from epcpy.epc_schemes.imovn import IMOVN
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta


class TestIMOVNInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=IMOVN,
    valid_data=[
        {
            "name": "test_valid_imovn_1",
            "uri": "urn:epc:id:imovn:9176187",
        },
        {
            "name": "test_valid_imovn_2",
            "uri": "urn:epc:id:imovn:0123456",
        },
        {
            "name": "test_valid_imovn_3",
            "uri": "urn:epc:id:imovn:0000000",
        },
        {
            "name": "test_valid_imovn_4",
            "uri": "urn:epc:id:imovn:9999999",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_imovn_identifier",
            "uri": "urn:epc:id:imvn:9176187",
        },
        {
            "name": "test_invalid_imovn_too_long",
            "uri": "urn:epc:id:imovn:91761877",
        },
        {
            "name": "test_invalid_imovn_too_short",
            "uri": "urn:epc:id:imovn:917618",
        },
        {
            "name": "test_invalid_imovn_invalid_chars",
            "uri": "urn:epc:id:imovn:91761A7",
        },
    ],
):
    pass
