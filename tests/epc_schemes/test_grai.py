import unittest

from epcpy.epc_schemes.grai import GRAI, GRAIFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1ElementMeta,
    TestTagEncodableMeta,
)


class TestGRAIInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GRAI,
    valid_data=[
        {
            "name": "test_valid_grai_1",
            "uri": "urn:epc:id:grai:0614141.12345.400",
        },
        {
            "name": "test_valid_grai_2",
            "uri": "urn:epc:id:grai:0614141.12345.4000000000000000",
        },
        {
            "name": "test_valid_grai_3",
            "uri": "urn:epc:id:grai:061414113245..0",
        },
        {
            "name": "test_valid_grai_4",
            "uri": "urn:epc:id:grai:061414113245..01",
        },
        {
            "name": "test_valid_grai_5",
            "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%2F",
        },
        {
            "name": "test_valid_grai_6",
            "uri": "urn:epc:id:grai:061414113245..274877906944",
        },
        {
            "name": "test_valid_grai_7",
            "uri": "urn:epc:id:grai:0614141.12345.ABCDEFGHIJKLMNOP",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_grai_identifier",
            "uri": "urn:epc:id:gai:0614141.12345.400",
        },
        {
            "name": "test_invalid_grai_too_long_serial_1",
            "uri": "urn:epc:id:grai:0614141.12345.40000000000000000",
        },
        {
            "name": "test_invalid_grai_invalid_company_pref_1",
            "uri": "urn:epc:id:grai:0614141132456..0",
        },
        {
            "name": "test_invalid_grai_invalid_company_pref_2",
            "uri": "urn:epc:id:grai:06141.6789012.01",
        },
        {
            "name": "test_invalid_grai_invalid_char",
            "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%23",
        },
        {
            "name": "test_invalid_grai_invalid_serial_1",
            "uri": "urn:epc:id:grai:061414113245..",
        },
        {
            "name": "test_invalid_grai_invalid_serial_2",
            "uri": "urn:epc:id:grai:0614141.12345.ABCDEFGHIJKLMNOPQ",
        },
    ],
):
    pass


class TestGRAIGS1Key(
    unittest.TestCase,
    metaclass=TestGS1ElementMeta,
    scheme=GRAI,
    valid_data=[
        {
            "name": "test_valid_grai_gs1_key_1",
            "uri": "urn:epc:id:grai:0614141.12345.400",
            "gs1_key": "0614141123452400",
            "gs1_element_string": "(8003)00614141123452400",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_grai_gs1_key_2",
            "uri": "urn:epc:id:grai:0614141.12345.4000000000000000",
            "gs1_key": "06141411234524000000000000000",
            "gs1_element_string": "(8003)006141411234524000000000000000",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_grai_gs1_key_3",
            "uri": "urn:epc:id:grai:061414113245..0",
            "gs1_key": "06141411324540",
            "gs1_element_string": "(8003)006141411324540",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_grai_gs1_key_4",
            "uri": "urn:epc:id:grai:061414113245..01",
            "gs1_key": "061414113245401",
            "gs1_element_string": "(8003)0061414113245401",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_grai_gs1_key_5",
            "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%2F",
            "gs1_key": "0614141123452ABCD1234/",
            "gs1_element_string": "(8003)00614141123452ABCD1234/",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_grai_gs1_key_6",
            "uri": "urn:epc:id:grai:061414113245..274877906944",
            "gs1_key": "0614141132454274877906944",
            "gs1_element_string": "(8003)00614141132454274877906944",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_grai_gs1_key_7",
            "uri": "urn:epc:id:grai:0614141.12345.ABCDEFGHIJKLMNOP",
            "gs1_key": "0614141123452ABCDEFGHIJKLMNOP",
            "gs1_element_string": "(8003)00614141123452ABCDEFGHIJKLMNOP",
            "company_prefix_length": 7,
        },
    ],
    invalid_data=[],
):
    pass


class TestGRAITagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=GRAI,
    valid_data=[
        {
            "name": "test_valid_grai_tag_encodable_1",
            "uri": "urn:epc:id:grai:0614141.12345.400",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.RESERVED_5,
            },
            "tag_uri": "urn:epc:tag:grai-96:5.0614141.12345.400",
            "hex": "33B4257BF40C0E4000000190",
        },
        {
            "name": "test_valid_grai_tag_encodable_2",
            "uri": "urn:epc:id:grai:0614141.12345.4000000000000000",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_170,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:grai-170:0.0614141.12345.4000000000000000",
            "hex": "3714257BF40C0E5A3060C183060C183060C183060C00",
        },
        {
            "name": "test_valid_grai_tag_encodable_3",
            "uri": "urn:epc:id:grai:061414113245..0",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:grai-96:0.061414113245..0",
            "hex": "3300393243FF740000000000",
        },
        {
            "name": "test_valid_grai_tag_encodable_4",
            "uri": "urn:epc:id:grai:061414113245..01",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_170,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:grai-170:0.061414113245..01",
            "hex": "3700393243FF74183100000000000000000000000000",
        },
        {
            "name": "test_valid_grai_tag_encodable_5",
            "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%2F",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_170,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:grai-170:0.0614141.12345.ABCD1234%2F",
            "hex": "3714257BF40C0E60C287118B266D1780000000000000",
        },
        {
            "name": "test_valid_grai_tag_encodable_6",
            "uri": "urn:epc:id:grai:061414113245..274877906943",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:grai-96:0.061414113245..274877906943",
            "hex": "3300393243FF743FFFFFFFFF",
        },
        {
            "name": "test_valid_grai_tag_encodable_7",
            "uri": "urn:epc:id:grai:0614141.12345.ABCDEFGHIJKLMNOP",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_170,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:grai-170:0.0614141.12345.ABCDEFGHIJKLMNOP",
            "hex": "3714257BF40C0E60C287122C68F224CA97326CE9F400",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_grai_serial_1",
            "uri": "urn:epc:id:grai:0614141.12345.4000000000000000",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_grai_serial_2",
            "uri": "urn:epc:id:grai:061414113245..01",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_grai_tag_encodable_serial_3",
            "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%2F",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_valid_grai_tag_encodable_serial_4",
            "uri": "urn:epc:id:grai:061414113245..274877906944",
            "kwargs": {
                "binary_coding_scheme": GRAI.BinaryCodingScheme.GRAI_96,
                "filter_value": GRAIFilterValue.ALL_OTHERS,
            },
        },
    ],
):
    pass
