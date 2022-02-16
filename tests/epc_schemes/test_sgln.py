import unittest

from epcpy.epc_schemes.sgln import SGLN, SGLNFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestSGLNInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=SGLN,
    valid_data=[
        {
            "name": "test_valid_sgln_1",
            "uri": "urn:epc:id:sgln:0614141.12345.400",
        },
        {
            "name": "test_valid_sgln_2",
            "uri": "urn:epc:id:sgln:0614141.12345.0",
        },
        {
            "name": "test_valid_sgln_3",
            "uri": "urn:epc:id:sgln:0614141.12345.01",
        },
        {
            "name": "test_valid_sgln_4",
            "uri": "urn:epc:id:sgln:061411.012345.01",
        },
        {
            "name": "test_valid_sgln_5",
            "uri": "urn:epc:id:sgln:061411123456..01",
        },
        {
            "name": "test_valid_sgln_6",
            "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQR",
        },
        {
            "name": "test_valid_sgln_7",
            "uri": "urn:epc:id:sgln:061411123456..2199023255552",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sgln_identifier",
            "uri": "urn:epc:id:sgn:0614141.12345.400",
        },
        {
            "name": "test_invalid_sgln_company_prefix_1",
            "uri": "urn:epc:id:sgln:06141.1234567.400",
        },
        {
            "name": "test_invalid_sgln_company_prefix_2",
            "uri": "urn:epc:id:sgln:0614112222222..400",
        },
        {
            "name": "test_invalid_sgln_serial_too_long",
            "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQRS",
        },
        {
            "name": "test_invalid_sgln_serial_too_short",
            "uri": "urn:epc:id:sgln:0614141.12345.",
        },
    ],
):
    pass


class TestSGLNGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=SGLN,
    valid_data=[
        {
            "name": "test_valid_sgln_gs1_key_1",
            "uri": "urn:epc:id:sgln:0614141.12345.400",
            "gs1_key": "0614141123452",
        },
        {
            "name": "test_valid_sgln_gs1_key_2",
            "uri": "urn:epc:id:sgln:0614141.12345.0",
            "gs1_key": "0614141123452",
        },
        {
            "name": "test_valid_sgln_gs1_key_3",
            "uri": "urn:epc:id:sgln:0614141.12345.01",
            "gs1_key": "0614141123452",
        },
        {
            "name": "test_valid_sgln_gs1_key_4",
            "uri": "urn:epc:id:sgln:061411.012345.01",
            "gs1_key": "0614110123452",
        },
        {
            "name": "test_valid_sgln_gs1_key_5",
            "uri": "urn:epc:id:sgln:061411123456..01",
            "gs1_key": "0614111234560",
        },
        {
            "name": "test_valid_sgln_gs1_key_6",
            "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQR",
            "gs1_key": "0614111234560",
        },
        {
            "name": "test_valid_sgln_gs1_key_7",
            "uri": "urn:epc:id:sgln:061411123456..2199023255552",
            "gs1_key": "0614111234560",
        },
    ],
    invalid_data=[],
):
    pass


class TestSGLNTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=SGLN,
    valid_data=[
        {
            "name": "test_valid_sgln_tag_encodable_1",
            "uri": "urn:epc:id:sgln:0614141.12345.400",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_96,
                "filter_value": SGLNFilterValue.RESERVED_1,
            },
            "tag_uri": "urn:epc:tag:sgln-96:1.0614141.12345.400",
            "hex": "3234257BF460720000000190",
        },
        {
            "name": "test_valid_sgln_tag_encodable_2",
            "uri": "urn:epc:id:sgln:0614141.12345.0",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_195,
                "filter_value": SGLNFilterValue.RESERVED_1,
            },
            "tag_uri": "urn:epc:tag:sgln-195:1.0614141.12345.0",
            "hex": "3934257BF46072C0000000000000000000000000000000000000",
        },
        {
            "name": "test_valid_sgln_tag_encodable_3",
            "uri": "urn:epc:id:sgln:0614141.12345.01",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_195,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgln-195:0.0614141.12345.01",
            "hex": "3914257BF46072C1880000000000000000000000000000000000",
        },
        {
            "name": "test_valid_sgln_tag_encodable_4",
            "uri": "urn:epc:id:sgln:061411.012345.01",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_195,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgln-195:0.061411.012345.01",
            "hex": "39183BF8C06072C1880000000000000000000000000000000000",
        },
        {
            "name": "test_valid_sgln_tag_encodable_5",
            "uri": "urn:epc:id:sgln:061411123456..01",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_195,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgln-195:0.061411123456..01",
            "hex": "390039318D8400C1880000000000000000000000000000000000",
        },
        {
            "name": "test_valid_sgln_tag_encodable_6",
            "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQR",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_195,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgln-195:0.061411123456..A%2F-BCDEFGHIJKLMNOPQR",
            "hex": "390039318D8401057AD850E2458D1E449952E64D9D3E851A4000",
        },
        {
            "name": "test_valid_sgln_tag_encodable_7",
            "uri": "urn:epc:id:sgln:061411123456..2199023255551",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_96,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgln-96:0.061411123456..2199023255551",
            "hex": "320039318D8401FFFFFFFFFF",
        },
        {
            "name": "test_valid_sgln_tag_encodable_8",
            "uri": "urn:epc:id:sgln:061411123456..2199023255552",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_195,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:sgln-195:0.061411123456..2199023255552",
            "hex": "390039318D8400C98B972C193364D5AB56AC8000000000000000",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sgln_tag_encodable_invalid_serial_1",
            "uri": "urn:epc:id:sgln:0614141.12345.01",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_96,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_sgln_tag_encodable_invalid_serial_2",
            "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQR",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_96,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_sgln_tag_encodable_invalid_serial_3",
            "uri": "urn:epc:id:sgln:061411123456..2199023255552",
            "kwargs": {
                "binary_coding_scheme": SGLN.BinaryCodingScheme.SGLN_96,
                "filter_value": SGLNFilterValue.ALL_OTHERS,
            },
        },
    ],
):
    pass
