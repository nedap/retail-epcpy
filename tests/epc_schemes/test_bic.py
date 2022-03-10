import unittest

from epcpy.epc_schemes.bic import BIC
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta


class TestBICInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=BIC,
    valid_data=[
        {
            "name": "test_valid_bic_1",
            "uri": "urn:epc:id:bic:CSQU3054383",
        },
        {
            "name": "test_valid_bic_2",
            "uri": "urn:epc:id:bic:CSQJ3054381",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_bic_too_long",
            "uri": "urn:epc:id:bic:CSQJ30543831",
        },
        {
            "name": "test_invalid_bic_wrong_catid",
            "uri": "urn:epc:id:bic:CSQA3054383",
        },
        {
            "name": "test_invalid_bic_too_many_chars",
            "uri": "urn:epc:id:bic:CSQJA054383",
        },
        {
            "name": "test_invalid_bic_wrong_ownercode",
            "uri": "urn:epc:id:bic:CSIJ3054381",
        },
    ],
):
    pass
