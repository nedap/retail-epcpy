import unittest

from epcpy.epc_pure_identities.gid import GID
from tests.epc_pure_identities.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestTagEncodableMeta,
)


class TestGIDInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GID,
    valid_data=[
        {
            "name": "test_valid_gid_1",
            "uri": "urn:epc:id:gid:95100000.12345.400",
        },
        {
            "name": "test_valid_gid_2",
            "uri": "urn:epc:id:gid:95100000.12345.0",
        },
        {
            "name": "test_valid_gid_3",
            "uri": "urn:epc:id:gid:0.0.0",
        },
        {
            "name": "test_valid_gid_4",
            "uri": "urn:epc:id:gid:268435455.16777215.68719476735",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_gid_identifier",
            "uri": "urn:epc:id:gi:0614141.123456.0",
        },
        {
            "name": "test_invalid_gid_serial_starting_with_zero",
            "uri": "urn:epc:id:gid:95100000.12345.01",
        },
        {
            "name": "test_invalid_gid_no_object",
            "uri": "urn:epc:id:gid:95100000..10",
        },
        {
            "name": "test_invalid_gid_no_manager",
            "uri": "urn:epc:id:gid:.0.0",
        },
        {
            "name": "test_invalid_gid_manager_starting_with_zero",
            "uri": "urn:epc:id:gid:01.0.0",
        },
        {
            "name": "test_invalid_gid_object_starting_with_zero",
            "uri": "urn:epc:id:gid:0.01.0",
        },
        {
            "name": "test_invalid_gid_serial_too_high",
            "uri": "urn:epc:id:gid:268435455.16777215.68719476736",
        },
        {
            "name": "test_invalid_gid_manager_too_high",
            "uri": "urn:epc:id:gid:268435456.16777215.68719476735",
        },
        {
            "name": "test_invalid_gid_object_too_high",
            "uri": "urn:epc:id:gid:268435455.16777216.68719476735",
        },
    ],
):
    pass


class TestGIDTagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=GID,
    valid_data=[
        {
            "name": "test_valid_gid_tag_encodable_1",
            "uri": "urn:epc:id:gid:95100000.12345.400",
            "tag_uri": "urn:epc:tag:gid-96:95100000.12345.400",
            "hex": "355AB1C60003039000000190",
        },
        {
            "name": "test_valid_gid_tag_encodable_2",
            "uri": "urn:epc:id:gid:95100000.12345.0",
            "tag_uri": "urn:epc:tag:gid-96:95100000.12345.0",
            "hex": "355AB1C60003039000000000",
        },
        {
            "name": "test_valid_gid_tag_encodable_3",
            "uri": "urn:epc:id:gid:0.0.0",
            "tag_uri": "urn:epc:tag:gid-96:0.0.0",
            "hex": "350000000000000000000000",
        },
        {
            "name": "test_valid_gid_tag_encodable_4",
            "uri": "urn:epc:id:gid:268435455.16777215.68719476735",
            "tag_uri": "urn:epc:tag:gid-96:268435455.16777215.68719476735",
            "hex": "35FFFFFFFFFFFFFFFFFFFFFF",
        },
    ],
    invalid_data=[],
):
    pass
