import unittest

from epcpy.epc_pure_identities.gdti import GDTI, GDTIFilterValue
from tests.epc_pure_identities.test_base_scheme import (
    TestEPCSchemeInitMeta,
    TestGS1KeyedMeta,
    TestTagEncodableMeta,
)


class TestGDTIInit(
    unittest.TestCase,
    metaclass=TestEPCSchemeInitMeta,
    scheme=GDTI,
    valid_data=[
        {
            "name": "test_valid_gdti_1",
            "uri": "urn:epc:id:gdti:0614141.12345.400",
        },
        {
            "name": "test_valid_gdti_2",
            "uri": "urn:epc:id:gdti:0614141.12345.40000000000000000",
        },
        {
            "name": "test_valid_gdti_3",
            "uri": "urn:epc:id:gdti:061414.123451.40000000000000000",
        },
        {
            "name": "test_valid_gdti_4",
            "uri": "urn:epc:id:gdti:0614141.12345.0",
        },
        {
            "name": "test_valid_gdti_5",
            "uri": "urn:epc:id:gdti:0614141.12345.ABCD1234%2F",
        },
        {
            "name": "test_valid_gdti_6",
            "uri": "urn:epc:id:gdti:0614141.12345.01",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_gdti_identifier",
            "uri": "urn:epc:id:gti:0614141.12345.40000000000000000",
        },
        {
            "name": "test_invalid_gdti_serial_too_long",
            "uri": "urn:epc:id:gdti:0614141.12345.400000000000000000",
        },
        {
            "name": "test_invalid_gdti_too_many_digits",
            "uri": "urn:epc:id:gdti:0614141.123456.40000000000000000",
        },
        {
            "name": "test_invalid_gdti_illegal_serial",
            "uri": "urn:epc:id:gdti:0614141.12345.ABCD1%23234%2F",
        },
        {
            "name": "test_invalid_gdti_invalid_company_pref",
            "uri": "urn:epc:id:gdti:06141.1123451.40000000000000000",
        },
    ],
):
    pass


class TestGDTIGS1Key(
    unittest.TestCase,
    metaclass=TestGS1KeyedMeta,
    scheme=GDTI,
    valid_data=[
        {
            "name": "test_valid_gdti_gs1_key_1",
            "uri": "urn:epc:id:gdti:0614141.12345.ABCD1234%2F",
            "gs1_key": "0614141123452ABCD1234/",
        },
        {
            "name": "test_valid_gdti_gs1_key_2",
            "uri": "urn:epc:id:gdti:0614141.12345.40000000000000000",
            "gs1_key": "061414112345240000000000000000",
        },
        {
            "name": "test_valid_gdti_gs1_key_3",
            "uri": "urn:epc:id:gdti:0614141.12345.0",
            "gs1_key": "06141411234520",
        },
        {
            "name": "test_valid_gdti_gs1_key_4",
            "uri": "urn:epc:id:gdti:061414.123451.40000000000000000",
            "gs1_key": "061414123451640000000000000000",
        },
    ],
    invalid_data=[],
):
    pass


class TestGDTITagEncodable(
    unittest.TestCase,
    metaclass=TestTagEncodableMeta,
    scheme=GDTI,
    valid_data=[
        {
            "name": "test_valid_gdti_tag_encodable_1",
            "uri": "urn:epc:id:gdti:0614141.12345.ABCD1234%2F",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_174,
                "filter_value": GDTIFilterValue.ALL_OTHERS,
            },
            "tag_uri": "urn:epc:tag:gdti-174:0.0614141.12345.ABCD1234%2F",
            "hex": "3E14257BF460730614388C593368BC00000000000000",
        },
        {
            "name": "test_valid_gdti_tag_encodable_2",
            "uri": "urn:epc:id:gdti:0614141.12345.2199023255551",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_96,
                "filter_value": GDTIFilterValue.RESERVED_2,
            },
            "tag_uri": "urn:epc:tag:gdti-96:2.0614141.12345.2199023255551",
            "hex": "2C54257BF46073FFFFFFFFFF",
        },
        {
            "name": "test_valid_gdti_tag_encodable_3",
            "uri": "urn:epc:id:gdti:0614141.12345.2199023255552",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_174,
                "filter_value": GDTIFilterValue.RESERVED_2,
            },
            "tag_uri": "urn:epc:tag:gdti-174:2.0614141.12345.2199023255552",
            "hex": "3E54257BF46072C98B972C193364D5AB56AC80000000",
        },
        {
            "name": "test_valid_gdti_tag_encodable_4",
            "uri": "urn:epc:id:gdti:0614141.12345.0",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_96,
                "filter_value": GDTIFilterValue.RESERVED_6,
            },
            "tag_uri": "urn:epc:tag:gdti-96:6.0614141.12345.0",
            "hex": "2CD4257BF460720000000000",
        },
    ],
    invalid_data=[
        {
            "name": "test_invalid_gdti_tag_encodable_invalid_serial_1",
            "uri": "urn:epc:id:gdti:0614141.12345.ABCD1234%2F",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_96,
                "filter_value": GDTIFilterValue.ALL_OTHERS,
            },
        },
        {
            "name": "test_invalid_gdti_tag_encodable_invalid_serial_2",
            "uri": "urn:epc:id:gdti:0614141.12345.2199023255552",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_96,
                "filter_value": GDTIFilterValue.RESERVED_2,
            },
        },
        {
            "name": "test_invalid_gdti_tag_encodable_invalid_serial_3",
            "uri": "urn:epc:id:gdti:0614141.12345.01",
            "kwargs": {
                "binary_coding_scheme": GDTI.BinaryCodingScheme.GDTI_96,
                "filter_value": GDTIFilterValue.RESERVED_2,
            },
        },
    ],
):
    pass
