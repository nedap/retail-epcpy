import unittest

from epcpy.epc_schemes.giai import GIAI, GIAIFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestGIAIInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GIAI,
    valid_data=[
        {
            "name": "test_valid_giai_1",
            "uri": "urn:epc:id:giai:0614141.12345400",
        },
        {
            "name": "test_valid_giai_2",
            "uri": "urn:epc:id:giai:0614141.0",
        },
        {
            "name": "test_valid_giai_3",
            "uri": "urn:epc:id:giai:0614141.1ABc%2FD",
        },
        {
            "name": "test_valid_giai_4",
            "uri": "urn:epc:id:giai:061411.01ABc%2FD",
        },
        {
            "name": "test_valid_giai_5",
            "uri": "urn:epc:id:giai:012345.012345678901234567890123",
        },
        {
            "name": "test_valid_giai_6",
            "uri": "urn:epc:id:giai:012345678901.012345678901234567",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_giai_identifier",
            "uri": "urn:epc:id:gai:061411.01ABc%2FD",
        },
        {
            "name": "test_invalid_giai_company_prefix_1",
            "uri": "urn:epc:id:giai:06141.1ABc%2FD",
        },
        {
            "name": "test_invalid_giai_company_prefix_2",
            "uri": "urn:epc:id:giai:0614111111111.1ABc%2FD",
        },
        {
            "name": "test_invalid_giai_serial_too_long_1",
            "uri": "urn:epc:id:giai:012345.0123456789012345678901234",
        },
        {
            "name": "test_invalid_giai_serial_too_long_1",
            "uri": "urn:epc:id:giai:012345.0123456789012345678901234",
        },
        {
            "name": "test_invalid_giai_serial_too_long_2",
            "uri": "urn:epc:id:giai:012345678901.0123456789012345678",
        },
    ],
):
    pass


class TestGIAIGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=GIAI,
    valid_data=[
        {
            "name": "test_valid_giai_gs1_key_1",
            "uri": "urn:epc:id:giai:0614141.12345400",
            "gs1_key": "061414112345400",
        },
        {
            "name": "test_valid_giai_gs1_key_2",
            "uri": "urn:epc:id:giai:0614141.0",
            "gs1_key": "06141410",
        },
        {
            "name": "test_valid_giai_gs1_key_3",
            "uri": "urn:epc:id:giai:0614141.1ABc%2FD",
            "gs1_key": "06141411ABc/D",
        },
        {
            "name": "test_valid_giai_gs1_key_4",
            "uri": "urn:epc:id:giai:061411.01ABc%2FD",
            "gs1_key": "06141101ABc/D",
        },
        {
            "name": "test_valid_giai_gs1_key_5",
            "uri": "urn:epc:id:giai:012345.012345678901234567890123",
            "gs1_key": "012345012345678901234567890123",
        },
        {
            "name": "test_valid_giai_gs1_key_6",
            "uri": "urn:epc:id:giai:012345678901.012345678901234567",
            "gs1_key": "012345678901012345678901234567",
        },
    ],
    invalid_data=[],
):
    pass


class TestGIAITagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=GIAI,
    valid_data=[
        {
            "name": "test_valid_giai_tag_encodable_1",
            "uri": "urn:epc:id:giai:0614141.12345400",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_202,
                "filter_value": GIAIFilterValue.RAIL_VEHICLE,
            },
            "tag_uri": "urn:epc:tag:giai-202:1.0614141.12345400",
            "hex": "3834257BF58B266D1AB460C00000000000000000000000000000",
        },
        {
            "name": "test_valid_giai_tag_encodable_2",
            "uri": "urn:epc:id:giai:0614141.0",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_96,
                "filter_value": GIAIFilterValue.RAIL_VEHICLE,
            },
            "tag_uri": "urn:epc:tag:giai-96:1.0614141.0",
            "hex": "3434257BF400000000000000",
        },
        {
            "name": "test_valid_giai_tag_encodable_3",
            "uri": "urn:epc:id:giai:0614141.1ABc%2FD",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_202,
                "filter_value": GIAIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:giai-202:0.0614141.1ABc%2FD",
            "hex": "3814257BF58C1858D7C400000000000000000000000000000000",
        },
        {
            "name": "test_valid_giai_tag_encodable_4",
            "uri": "urn:epc:id:giai:061411.01ABc%2FD",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_202,
                "filter_value": GIAIFilterValue.RESERVED_4,
            },
            "tag_uri": "urn:epc:tag:giai-202:4.061411.01ABc%2FD",
            "hex": "38983BF8D831830B1AF880000000000000000000000000000000",
        },
        {
            "name": "test_valid_giai_tag_encodable_5",
            "uri": "urn:epc:id:giai:012345.012345678901234567890123",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_202,
                "filter_value": GIAIFilterValue.RAIL_VEHICLE,
            },
            "tag_uri": "urn:epc:tag:giai-202:1.012345.012345678901234567890123",
            "hex": "38380C0E583164CDA356CDDC3960C593368D5B3770E583164CC0",
        },
        {
            "name": "test_valid_giai_tag_encodable_6",
            "uri": "urn:epc:id:giai:0614141.12345400",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_96,
                "filter_value": GIAIFilterValue.RAIL_VEHICLE,
            },
            "tag_uri": "urn:epc:tag:giai-96:1.0614141.12345400",
            "hex": "3434257BF400000000BC6038",
        },
        {
            "name": "test_valid_giai_tag_encodable_7",
            "uri": "urn:epc:id:giai:0614141.02",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_202,
                "filter_value": GIAIFilterValue.RAIL_VEHICLE,
            },
            "tag_uri": "urn:epc:tag:giai-202:1.0614141.02",
            "hex": "3834257BF5832000000000000000000000000000000000000000",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_giai_tag_encodable_invalid_serial_1",
            "uri": "urn:epc:id:giai:0614141.02",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_96,
                "filter_value": GIAIFilterValue.RAIL_VEHICLE,
            },
        },
        {
            "name": "test_invalid_giai_tag_encodable_invalid_serial_2",
            "uri": "urn:epc:id:giai:061411.11ABc%2FD",
            "kwargs": {
                "binary_coding_scheme": GIAI.BinaryCodingScheme.GIAI_96,
                "filter_value": GIAIFilterValue.RESERVED_4,
            },
        },
    ],
):
    pass
