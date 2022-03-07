import unittest

from epcpy.epc_pure_identities.adi import ADI, ADIFilterValue
from tests.epc_pure_identities.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestTagEncodableMeta,
)


class TestADIInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=ADI,
    valid_data=[
        {
            "name": "test_valid_adi_1",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.2WMA-52",
        },
        {
            "name": "test_valid_adi_2",
            "uri": "urn:epc:id:adi:2S194..12345678901",
        },
        {
            "name": "test_valid_adi_3",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.%232WMA52",
        },
        {
            "name": "test_valid_adi_4",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.%232WM%2FA52",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_adi_identifier",
            "uri": "urn:epc:id:aldi:W81X9C.3KL984PX1.2WMA52",
        },
        {
            "name": "test_invalid_adi_no_adi_char",
            "uri": "urn:epc:id:adi:2S194..%23",
        },
        {
            "name": "test_invalid_adi_percent23_wrong_location",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.2%232WMA52",
        },
        {
            "name": "test_invalid_adi_illegal_char",
            "uri": "urn:epc:id:adi:W81I9C.3KL984IPX1.2",
        },
        {
            "name": "test_invalid_adi_too_little_cagecode_or_dodaac",
            "uri": "urn:epc:id:adi:W89C.3KL984IPX1.2",
        },
        {
            "name": "test_invalid_adi_too_many_cagecode_or_dodaac",
            "uri": "urn:epc:id:adi:W8AAA9C.3KL984IPX1.2",
        },
        {
            "name": "test_invalid_adi_too_many_part_chars",
            "uri": "urn:epc:id:adi:W8AA9C.012345678901234567890123456789012.2",
        },
        {
            "name": "test_invalid_adi_too_many_serial_chars",
            "uri": "urn:epc:id:adi:W8AA9C.123.0123456789012345678901234567891",
        },
    ],
):
    pass


class TestADITagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=ADI,
    valid_data=[
        {
            "name": "test_valid_adi_tag_encodable_1",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.2WMA-52",
            "kwargs": {
                "filter_value": ADIFilterValue.RESERVED_5,
            },
            "tag_uri": "urn:epc:tag:adi-var:5.W81X9C.3KL984PX1.2WMA-52",
            "hex": "3B157E316390F32CCE78D106310325CD06DD7200",
        },
        {
            "name": "test_valid_adi_tag_encodable_2",
            "uri": "urn:epc:id:adi:2S194..12345678901",
            "kwargs": {
                "filter_value": ADIFilterValue.OTHER_REPAIR,
            },
            "tag_uri": "urn:epc:tag:adi-var:23.2S194..12345678901",
            "hex": "3B5E0C93C79D00C72CF4D76DF8E70C40",
        },
        {
            "name": "test_valid_adi_tag_encodable_3",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.%232WMA52",
            "kwargs": {
                "filter_value": ADIFilterValue.UNIT_LOAD_DEVICES,
            },
            "tag_uri": "urn:epc:tag:adi-var:12.W81X9C.3KL984PX1.%232WMA52",
            "hex": "3B317E316390F32CCE78D10631023C97341D7200",
        },
        {
            "name": "test_valid_adi_tag_encodable_4",
            "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.%232WM%2FA52",
            "kwargs": {
                "filter_value": ADIFilterValue.ITEM_OTHER,
            },
            "tag_uri": "urn:epc:tag:adi-var:1.W81X9C.3KL984PX1.%232WM%2FA52",
            "hex": "3B057E316390F32CCE78D10631023C9736F075C80000",
        },
    ],
    invalid_data=[],
):
    pass
