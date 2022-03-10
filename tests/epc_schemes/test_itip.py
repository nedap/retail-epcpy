import unittest

from epcpy.epc_schemes.itip import ITIP, ITIPFilterValue
from tests.epc_schemes.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestITIPInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=ITIP,
    valid_data=[
        {
            "name": "test_valid_itip_1",
            "uri": "urn:epc:id:itip:4012345.012345.01.02.987",
        },
        {
            "name": "test_valid_itip_2",
            "uri": "urn:epc:id:itip:0123456.012345.00.00.01234567890123456789",
        },
        {
            "name": "test_valid_itip_3",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.01234567890123456789",
        },
        {
            "name": "test_valid_itip_4",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_itip_identifier",
            "uri": "urn:epc:id:itp:012345678901.0.00.00.01234567890123456789",
        },
        {
            "name": "test_invalid_itip_serial_too_long",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.012345678901234567890",
        },
        {
            "name": "test_invalid_itip_no_serial",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.",
        },
        {
            "name": "test_invalid_itip_company_pref_1",
            "uri": "urn:epc:id:itip:01234.01234567.00.00.01234567890123456789",
        },
        {
            "name": "test_invalid_itip_company_pref_2",
            "uri": "urn:epc:id:itip:0123456789012.0.00.00.01234567890123456789",
        },
        {
            "name": "test_invalid_itip_invalid_piece_1",
            "uri": "urn:epc:id:itip:012345678901.0.0.00.ABCDEFGHIJKLMNOP%2FRST",
        },
        {
            "name": "test_invalid_itip_invalid_piece_2",
            "uri": "urn:epc:id:itip:012345678901.0.000.00.ABCDEFGHIJKLMNOP%2FRST",
        },
        {
            "name": "test_invalid_itip_invalid_total_1",
            "uri": "urn:epc:id:itip:012345678901.0.00.0.ABCDEFGHIJKLMNOP%2FRST",
        },
        {
            "name": "test_invalid_itip_invalid_total_2",
            "uri": "urn:epc:id:itip:012345678901.0.00.000.ABCDEFGHIJKLMNOP%2FRST",
        },
    ],
):
    pass


class TestITIPGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=ITIP,
    valid_data=[
        {
            "name": "test_valid_itip_gs1_element_string_1",
            "uri": "urn:epc:id:itip:4012345.012345.01.02.987",
            "gs1_element_string": "(8006)040123451234560102(21)987",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_itip_gs1_element_string_2",
            "uri": "urn:epc:id:itip:0123456.012345.00.00.01234567890123456789",
            "gs1_element_string": "(8006)001234561234580000(21)01234567890123456789",
            "company_prefix_length": 7,
        },
        {
            "name": "test_valid_itip_gs1_element_string_3",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.01234567890123456789",
            "gs1_element_string": "(8006)001234567890120000(21)01234567890123456789",
            "company_prefix_length": 12,
        },
        {
            "name": "test_valid_itip_gs1_element_string_4",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
            "gs1_element_string": "(8006)001234567890120000(21)ABCDEFGHIJKLMNOP/RST",
            "company_prefix_length": 12,
        },
    ],
    invalid_data=[],
):
    pass


class TestITIPTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=ITIP,
    valid_data=[
        {
            "name": "test_valid_itip_tag_encodable_1",
            "uri": "urn:epc:id:itip:4012345.012345.01.02.987",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_110,
                "filter_value": ITIPFilterValue.RESERVED_7,
            },
            "tag_uri": "urn:epc:tag:itip-110:7.4012345.012345.01.02.987",
            "hex": "40F4F4E4E40C0E40820000000F6C",
        },
        {
            "name": "test_valid_itip_tag_encodable_2",
            "uri": "urn:epc:id:itip:0123456.012345.00.00.01234567890123456789",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_212,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:itip-212:0.0123456.012345.00.00.01234567890123456789",
            "hex": "41140789000C0E400060C593368D5B3770E583164CDA356CDDC39000",
        },
        {
            "name": "test_valid_itip_tag_encodable_3",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.01234567890123456789",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_212,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:itip-212:0.012345678901.0.00.00.01234567890123456789",
            "hex": "41000B7F7070D4000060C593368D5B3770E583164CDA356CDDC39000",
        },
        {
            "name": "test_valid_itip_tag_encodable_4",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_212,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:itip-212:0.012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
            "hex": "41000B7F7070D40000830A1C48B1A3C8932A5CC9B3A7D05F4A9D4000",
        },
        {
            "name": "test_valid_itip_tag_encodable_5",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.274877906943",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_110,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:itip-110:0.012345678901.0.00.00.274877906943",
            "hex": "40000B7F7070D40000FFFFFFFFFC",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_itip_tag_encodable_invalid_serial_1",
            "uri": "urn:epc:id:itip:0123456.012345.00.00.01234567890123456789",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_110,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_itip_tag_encodable_invalid_serial_2",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_110,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_itip_tag_encodable_invalid_serial_3",
            "uri": "urn:epc:id:itip:012345678901.0.00.00.274877906944",
            "kwargs": {
                "binary_coding_scheme": ITIP.BinaryCodingScheme.ITIP_110,
                "filter_value": ITIPFilterValue.ALL_OTHERS,
            },
        },
    ],
):
    pass
