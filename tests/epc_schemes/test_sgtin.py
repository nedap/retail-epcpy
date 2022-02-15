import unittest

from epcpy.epc_schemes.sgtin import GTIN_TYPE, SGTIN, SGTINFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


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
        {
            "name": "test_valid_sgtin_3",
            "uri": "urn:epc:id:sgtin:507121923656.1..%25:.13%26",
        },
        {
            "name": "test_valid_sgtin_4",
            "uri": "urn:epc:id:sgtin:507124.1123456..%25:.13%26",
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
            "name": "test_invalid_sgtin_company_prefix_1",
            "uri": "urn:epc:id:sgtin:50712.11123456..%25:.13%26",
        },
        {
            "name": "test_invalid_sgtin_company_prefix_2",
            "uri": "urn:epc:id:sgtin:5071241234567.0..%25:.13%26",
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
            "gs1_key": "85071219236581",
        },
        {
            "name": "test_valid_sgtin_gs1_key_2",
            "uri": "urn:epc:id:sgtin:00000000000.00.0",
            "gs1_key": "00000000000000",
        },
        {
            "name": "test_valid_sgtin_gs1_key_3",
            "uri": "urn:epc:id:sgtin:5019265.123588..%25:.13%26",
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


class TestSGTINTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=SGTIN,
    valid_data=[
        {
            "name": "test_valid_sgtin_tag_encodable_1",
            "uri": "urn:epc:id:sgtin:50712192365.88..%25:.13%26",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_198,
                "filter_value": SGTINFilterValue.POS_ITEM,
            },
            "tag_uri": "urn:epc:tag:sgtin-198:1.50712192365.88..%25:.13%26",
            "hex": "362579D5D4ADB6172574B98B34C0000000000000000000000000",
        },
        {
            "name": "test_valid_sgtin_tag_encodable_2",
            "uri": "urn:epc:id:sgtin:50712192365.88..%25:.13%26",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_198,
                "filter_value": SGTINFilterValue.RESERVED_5,
            },
            "tag_uri": "urn:epc:tag:sgtin-198:5.50712192365.88..%25:.13%26",
            "hex": "36A579D5D4ADB6172574B98B34C0000000000000000000000000",
        },
        {
            "name": "test_valid_sgtin_tag_encodable_3",
            "uri": "urn:epc:id:sgtin:50712192365.88.0",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_96,
                "filter_value": SGTINFilterValue.UNIT_LOAD,
            },
            "tag_uri": "urn:epc:tag:sgtin-96:6.50712192365.88.0",
            "hex": "30C579D5D4ADB60000000000",
        },
        {
            "name": "test_valid_sgtin_tag_encodable_4",
            "uri": "urn:epc:id:sgtin:50712192365.88.0",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_198,
                "filter_value": SGTINFilterValue.UNIT_LOAD,
            },
            "tag_uri": "urn:epc:tag:sgtin-198:6.50712192365.88.0",
            "hex": "36C579D5D4ADB618000000000000000000000000000000000000",
        },
        {
            "name": "test_valid_sgtin_tag_encodable_default_filter",
            "uri": "urn:epc:id:sgtin:50712192365.88.156789012",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_96,
            },
            "tag_uri": "urn:epc:tag:sgtin-96:1.50712192365.88.156789012",
            "hex": "302579D5D4ADB60009586914",
        },
        {
            "name": "test_valid_sgtin_tag_encodable_default_coding_scheme",
            "uri": "urn:epc:id:sgtin:50712192365.88.112789012",
            "kwargs": {
                "filter_value": SGTINFilterValue.POS_ITEM,
            },
            "tag_uri": "urn:epc:tag:sgtin-96:1.50712192365.88.112789012",
            "hex": "302579D5D4ADB60006B90614",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_sgtin_tag_encodable_invalid_serial_for_coding_scheme_1",
            "uri": "urn:epc:id:sgtin:50712192365.88..%25:.13%26",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_96,
                "filter_value": SGTINFilterValue.POS_ITEM,
            },
        },
        {
            "name": "test_invalid_sgtin_tag_encodable_invalid_serial_for_coding_scheme_2",
            "uri": "urn:epc:id:sgtin:50712192365.88.0123",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_96,
                "filter_value": SGTINFilterValue.POS_ITEM,
            },
        },
        {
            "name": "test_invalid_sgtin_tag_encodable_invalid_serial_for_coding_scheme_3",
            "uri": "urn:epc:id:sgtin:50712192365.88.1123456789012",
            "kwargs": {
                "binary_coding_scheme": SGTIN.BinaryCodingScheme.SGTIN_96,
                "filter_value": SGTINFilterValue.POS_ITEM,
            },
        },
    ],
):
    pass
