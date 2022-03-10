import unittest

from epcpy.epc_schemes.pgln import PGLN
from tests.epc_schemes.test_base_scheme import TestEPCSchemeInitMeta, TestGS1KeyedMeta


class TestPGLNInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=PGLN,
    valid_data=[
        {
            "name": "test_valid_pgln_1",
            "uri": "urn:epc:id:pgln:1234567.89012",
        },
        {
            "name": "test_valid_pgln_2",
            "uri": "urn:epc:id:pgln:012345678901.",
        },
        {
            "name": "test_valid_pgln_3",
            "uri": "urn:epc:id:pgln:01234567890.0",
        },
        {
            "name": "test_valid_pgln_4",
            "uri": "urn:epc:id:pgln:0123456789.01",
        },
        {
            "name": "test_valid_pgln_5",
            "uri": "urn:epc:id:pgln:012345.012345",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_pgln_identifier",
            "uri": "urn:epc:id:gln:012345678901.",
        },
        {
            "name": "test_invalid_pgln_company_prefix_1",
            "uri": "urn:epc:id:pgln:01234.5678901",
        },
        {
            "name": "test_invalid_pgln_company_prefix_2",
            "uri": "urn:epc:id:pgln:0123456789012.",
        },
        {
            "name": "test_invalid_pgln_serial_too_long_1",
            "uri": "urn:epc:id:pgln:012345.5678901",
        },
        {
            "name": "test_invalid_pgln_serial_invalid_chars",
            "uri": "urn:epc:id:pgln:01234.567A01",
        },
    ],
):
    pass


class TestPGLNGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=PGLN,
    valid_data=[
        {
            "name": "test_valid_pgln_gs1_key_1",
            "uri": "urn:epc:id:pgln:1234567.89012",
            "gs1_key": "1234567890128",
            "gs1_element_string": "(417)1234567890128",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_pgln_gs1_key_2",
            "uri": "urn:epc:id:pgln:012345678901.",
            "gs1_key": "0123456789012",
            "gs1_element_string": "(417)0123456789012",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_pgln_gs1_key_3",
            "uri": "urn:epc:id:pgln:01234567890.0",
            "gs1_key": "0123456789005",
            "gs1_element_string": "(417)0123456789005",
            "company_prefix_length": 11,
        },
        {
            "name": "test_valid_pgln_gs1_key_4",
            "uri": "urn:epc:id:pgln:0123456789.01",
            "gs1_key": "0123456789012",
            "gs1_element_string": "(417)0123456789012",
            "company_prefix_length": 10,
        },
        {
            "name": "test_valid_pgln_gs1_key_5",
            "uri": "urn:epc:id:pgln:012345.012345",
            "gs1_key": "0123450123454",
            "gs1_element_string": "(417)0123450123454",
            "company_prefix_length": 6,
        },
    ],
    invalid_data=[],
):
    pass
