import unittest

from epcpy.epc_schemes.lgtin import GTIN_TYPE, LGTIN
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta, TestGS1ElementMeta


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


class TestLGTINGS1Key(
    unittest.TestCase,
    metaclass=TestGS1ElementMeta,
    scheme=LGTIN,
    valid_data=[
        {
            "name": "test_valid_lgtin_gs1_key_1",
            "uri": "urn:epc:class:lgtin:50712192365.88..%25:.13%26",
            "gs1_key": "85071219236581",
            "gs1_element_string": "(01)85071219236581(10).%:.13&",
            "company_prefix_length": 11,
        },
        {
            "name": "test_valid_lgtin_gs1_key_2",
            "uri": "urn:epc:class:lgtin:00000000000.00.0",
            "gs1_key": "00000000000000",
            "gs1_element_string": "(01)00000000000000(10)0",
            "company_prefix_length": 11,
        },
        {
            "name": "test_valid_lgtin_gs1_key_3",
            "uri": "urn:epc:class:lgtin:5019265.123588..%25:.13%26",
            "gs1_key": "15019265235883",
            "gs1_element_string": "(01)15019265235883(10).%:.13&",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_lgtin_gs1_key_4",
            "uri": "urn:epc:class:lgtin:00000950.01093.Serial",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
            "gs1_key": "0000095010939",
            "gs1_element_string": "(01)00000095010939(10)Serial",
            "company_prefix_length": 8,
        },
        {
            "name": "test_valid_lgtin_gs1_key_5",
            "uri": "urn:epc:class:lgtin:00000950.01093.Serial",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN12},
            "gs1_key": "000095010939",
            "gs1_element_string": "(01)00000095010939(10)Serial",
            "company_prefix_length": 8,
        },
        {
            "name": "test_valid_lgtin_gs1_key_6",
            "uri": "urn:epc:class:lgtin:00000950.01093.Serial",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
            "gs1_key": "95010939",
            "gs1_element_string": "(01)00000095010939(10)Serial",
            "company_prefix_length": 8,
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_lgtin_gs1_key_too_little_zeros_gtin13",
            "uri": "urn:epc:class:lgtin:5019265.123588..%25:.13%26",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
        },
        {
            "name": "test_invalid_lgtin_gs1_key_too_little_zeros_gtin12",
            "uri": "urn:epc:class:lgtin:1519265.023588..%25:.13%26",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN12},
        },
        {
            "name": "test_invalid_lgtin_gs1_key_too_little_zeros_gtin8",
            "uri": "urn:epc:class:lgtin:0000565.023588..%25:.13%26",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
        },
    ],
):
    pass
