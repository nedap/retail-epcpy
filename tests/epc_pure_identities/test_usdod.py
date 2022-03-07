import unittest

from epcpy.epc_pure_identities.usdod import USDOD, USDODFilterValue
from tests.epc_pure_identities.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestTagEncodableMeta,
)


class TestUSDODInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=USDOD,
    valid_data=[
        {
            "name": "test_valid_usdod_1",
            "uri": "urn:epc:id:usdod:2S194.12345678901",
        },
        {
            "name": "test_valid_usdod_2",
            "uri": "urn:epc:id:usdod:2S194.0",
        },
        {
            "name": "test_valid_usdod_3",
            "uri": "urn:epc:id:usdod:2S1941.0",
        },
        {
            "name": "test_valid_usdod_4",
            "uri": "urn:epc:id:usdod:2S194.68719476735",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_usdod_identifier",
            "uri": "urn:epc:id:dod:2S194.12345678901",
        },
        {
            "name": "test_invalid_usdod_serial_too_long",
            "uri": "urn:epc:id:usdod:2S194.123456789012",
        },
        {
            "name": "test_invalid_usdod_serial_too_high",
            "uri": "urn:epc:id:usdod:2S194.68719476736",
        },
        {
            "name": "test_invalid_usdod_cage_code_length_1",
            "uri": "urn:epc:id:usdod:2S19.68719476735",
        },
        {
            "name": "test_invalid_usdod_cage_code_length_2",
            "uri": "urn:epc:id:usdod:2S19411.68719476735",
        },
        {
            "name": "test_invalid_usdod_cage_code_chars",
            "uri": "urn:epc:id:usdod:2S1I1.68719476735",
        },
    ],
):
    pass


class TestUSDODTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=USDOD,
    valid_data=[
        {
            "name": "test_valid_usdod_tag_encodable_1",
            "uri": "urn:epc:id:usdod:2S194.12345678901",
            "kwargs": {
                "filter_value": USDODFilterValue.PALLET,
            },
            "tag_uri": "urn:epc:tag:usdod-96:0.2S194.12345678901",
            "hex": "2F02032533139342DFDC1C35",
        },
        {
            "name": "test_valid_usdod_tag_encodable_2",
            "uri": "urn:epc:id:usdod:2S194.0",
            "kwargs": {
                "filter_value": USDODFilterValue.CASE,
            },
            "tag_uri": "urn:epc:tag:usdod-96:1.2S194.0",
            "hex": "2F1203253313934000000000",
        },
        {
            "name": "test_valid_usdod_tag_encodable_3",
            "uri": "urn:epc:id:usdod:2S1941.0",
            "kwargs": {
                "filter_value": USDODFilterValue.UNIT_PACK,
            },
            "tag_uri": "urn:epc:tag:usdod-96:2.2S1941.0",
            "hex": "2F2325331393431000000000",
        },
        {
            "name": "test_valid_usdod_tag_encodable_4",
            "uri": "urn:epc:id:usdod:2S194.68719476735",
            "kwargs": {
                "filter_value": USDODFilterValue.RESERVED_15,
            },
            "tag_uri": "urn:epc:tag:usdod-96:15.2S194.68719476735",
            "hex": "2FF203253313934FFFFFFFFF",
        },
    ],
    invalid_data=[],
):
    pass
