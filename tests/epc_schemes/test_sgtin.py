import unittest

from epcpy.epc_schemes.sgtin import GTIN_TYPE, SGTIN
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta, TestGS1KeyedMeta


class TestSGTINInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=SGTIN,
    valid_data=[
        {
            "name": "test_valid_sgtin_1",
            "uri": "urn:epc:id:sgtin:50712192365.88..%25:.13%26",
        },
        {
            "name": "test_valid_sgtin_2",
            "uri": "urn:epc:id:sgtin:00000000000.00.0",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sgtin_hex_serial",
            "uri": "urn:epc:id:sgtin:50712192365.88..%23:.13%26",
        },
        {
            "name": "test_invalid_sgtin_identifier",
            "uri": "urn:epc:id:sg:50712192365.88..%25:.13%26",
        },
        {
            "name": "test_invalid_sgtin_too_many_digits",
            "uri": "urn:epc:id:sgtin:000000000000.00.0",
        },
        {
            "name": "test_invalid_sgtin_missing_semicolon",
            "uri": "urn:epcid:sgtin:00000000000.00.0",
        },
        {
            "name": "test_invalid_sgtin_serial_too_large",
            "uri": "urn:epc:id:sgtin:00000000000.00.123456789012345678901",
        },
    ],
):
    pass


class TestSGTINGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=SGTIN,
    valid_data=[
        {
            "name": "test_valid_sgtin_gs1_key_1",
            "uri": "urn:epc:id:sgtin:50712192365.88..%25:.13%26",
            "kwargs": {},
            "gs1_key": "85071219236581",
        },
        {
            "name": "test_valid_sgtin_gs1_key_2",
            "uri": "urn:epc:id:sgtin:00000000000.00.0",
            "kwargs": {},
            "gs1_key": "00000000000000",
        },
        {
            "name": "test_valid_sgtin_gs1_key_3",
            "uri": "urn:epc:id:sgtin:5019265.123588..%25:.13%26",
            "kwargs": {},
            "gs1_key": "15019265235883",
        },
        {
            "name": "test_valid_sgtin_gs1_key_4",
            "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
            "gs1_key": "0000095010939",
        },
        {
            "name": "test_valid_sgtin_gs1_key_5",
            "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN12},
            "gs1_key": "000095010939",
        },
        {
            "name": "test_valid_sgtin_gs1_key_6",
            "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
            "gs1_key": "95010939",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sgtin_gs1_key_too_little_zeros_gtin13",
            "uri": "urn:epc:id:sgtin:5019265.123588..%25:.13%26",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
        },
        {
            "name": "test_invalid_sgtin_gs1_key_too_little_zeros_gtin12",
            "uri": "urn:epc:id:sgtin:1519265.023588..%25:.13%26",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN12},
        },
        {
            "name": "test_invalid_sgtin_gs1_key_too_little_zeros_gtin8",
            "uri": "urn:epc:id:sgtin:0000565.023588..%25:.13%26",
            "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
        },
    ],
):
    pass
