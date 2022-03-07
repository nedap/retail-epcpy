import unittest

from epcpy.epc_classes.lgtin import LGTIN
from tests.epc_pure_identities.test_base_scheme import TestEPCSchemeInitMeta


class TestLGTINInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=LGTIN,
    valid_data=[
        {
            "name": "test_valid_lgtin_1",
            "uri": "urn:epc:class:lgtin:061414.0123456.xyz3311cba",
        },
        {
            "name": "test_valid_lgtin_2",
            "uri": "urn:epc:class:lgtin:061414012345.0.0",
        },
        {
            "name": "test_valid_lgtin_3",
            "uri": "urn:epc:class:lgtin:061414012345.0.01234567890123456789",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_lgtin_identifier",
            "uri": "urn:epc:class:lgtn:06141.10123456.xyz3311cba",
        },
        {
            "name": "test_invalid_lgtin_company_prefix_1",
            "uri": "urn:epc:class:lgtin:06141.10123456.01ABc%2FD",
        },
        {
            "name": "test_invalid_lgtin_company_prefix_2",
            "uri": "urn:epc:class:lgtin:0614140123456.0.1",
        },
        {
            "name": "test_invalid_lgtin_invalid_component",
            "uri": "urn:epc:class:lgtin:06141.0.01ABc%2FD",
        },
        {
            "name": "test_invalid_lgtin_serial_too_long_1",
            "uri": "urn:epc:class:lgtin:012345.0123456.012345678901234567890",
        },
    ],
):
    pass
