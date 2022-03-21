import unittest

from epcpy import (
    epc_pure_identity_to_gs1_element,
    epc_pure_identity_to_gs1_element_string,
    epc_pure_identity_to_gs1_key,
    epc_pure_identity_to_gs1_keyed,
    epc_pure_identity_to_scheme,
    epc_pure_identity_to_tag_encodable,
    get_gs1_key,
    hex_to_tag_encodable,
    tag_uri_to_tag_encodable,
)
from epcpy.epc_schemes.adi import ADI
from epcpy.epc_schemes.bic import BIC
from epcpy.epc_schemes.cpi import CPI
from epcpy.epc_schemes.gdti import GDTI
from epcpy.epc_schemes.giai import GIAI
from epcpy.epc_schemes.gid import GID
from epcpy.epc_schemes.ginc import GINC
from epcpy.epc_schemes.grai import GRAI
from epcpy.epc_schemes.gsin import GSIN
from epcpy.epc_schemes.gsrn import GSRN
from epcpy.epc_schemes.gsrnp import GSRNP
from epcpy.epc_schemes.imovn import IMOVN
from epcpy.epc_schemes.itip import ITIP
from epcpy.epc_schemes.pgln import PGLN
from epcpy.epc_schemes.sgcn import SGCN
from epcpy.epc_schemes.sgln import SGLN
from epcpy.epc_schemes.sgtin import GTIN_TYPE, SGTIN
from epcpy.epc_schemes.sscc import SSCC
from epcpy.epc_schemes.upui import UPUI
from epcpy.epc_schemes.usdod import USDOD
from epcpy.utils.common import ConvertException

VALID_TEST_DATA = [
    {
        "scheme": ADI,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:adi:W81X9C.3KL984PX1.2WMA-52",
        "tag_uri": "urn:epc:tag:adi-var:5.W81X9C.3KL984PX1.2WMA-52",
        "hex": "3B157E316390F32CCE78D106310325CD06DD7200",
    },
    {
        "scheme": BIC,
        "tag_encodable": False,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:bic:CSQJ3054381",
    },
    {
        "scheme": CPI,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": True,
        "uri": "urn:epc:id:cpi:0614141.12-456.123456789",
        "gs1_element_string": "(8010)061414112-456(8011)123456789",
        "tag_uri": "urn:epc:tag:cpi-var:0.0614141.12-456.123456789",
        "hex": "3D14257BF71CADD35D8000075BCD1500",
    },
    {
        "scheme": GDTI,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gdti:0614141.12345.ABCD1234%2F",
        "gs1_key": "0614141123452ABCD1234/",
        "gs1_element_string": "(253)0614141123452ABCD1234/",
        "company_prefix_length": 7,
        "tag_uri": "urn:epc:tag:gdti-174:0.0614141.12345.ABCD1234%2F",
        "hex": "3E14257BF460730614388C593368BC00000000000000",
    },
    {
        "scheme": GIAI,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:giai:0614141.1ABc%2FD",
        "gs1_key": "06141411ABc/D",
        "gs1_element_string": "(8004)06141411ABc/D",
        "company_prefix_length": 7,
        "tag_uri": "urn:epc:tag:giai-202:0.0614141.1ABc%2FD",
        "hex": "3814257BF58C1858D7C400000000000000000000000000000000",
    },
    {
        "scheme": GID,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:gid:268435455.16777215.68719476735",
        "tag_uri": "urn:epc:tag:gid-96:268435455.16777215.68719476735",
        "hex": "35FFFFFFFFFFFFFFFFFFFFFF",
    },
    {
        "scheme": GINC,
        "tag_encodable": False,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:ginc:061411.01ABc%2FD",
        "gs1_key": "06141101ABc/D",
        "gs1_element_string": "(401)06141101ABc/D",
        "company_prefix_length": 6,
    },
    {
        "scheme": GRAI,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:grai:0614141.12345.ABCD1234%2F",
        "gs1_key": "0614141123452ABCD1234/",
        "gs1_element_string": "(8003)00614141123452ABCD1234/",
        "company_prefix_length": 7,
        "tag_uri": "urn:epc:tag:grai-170:0.0614141.12345.ABCD1234%2F",
        "hex": "3714257BF40C0E60C287118B266D1780000000000000",
    },
    {
        "scheme": GSIN,
        "tag_encodable": False,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gsin:061414.0123456789",
        "gs1_key": "06141401234567891",
        "gs1_element_string": "(402)06141401234567891",
        "company_prefix_length": 6,
    },
    {
        "scheme": GSRN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gsrn:012345678901.01234",
        "gs1_key": "012345678901012342",
        "gs1_element_string": "(8018)012345678901012342",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:gsrn-96:0.012345678901.01234",
        "hex": "2D000B7F7070D404D2000000",
    },
    {
        "scheme": GSRNP,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:gsrnp:012345678901.01234",
        "gs1_key": "012345678901012342",
        "gs1_element_string": "(8017)012345678901012342",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:gsrnp-96:0.012345678901.01234",
        "hex": "2E000B7F7070D404D2000000",
    },
    {
        "scheme": IMOVN,
        "tag_encodable": False,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:imovn:9176187",
    },
    {
        "scheme": ITIP,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": True,
        "uri": "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
        "gs1_element_string": "(8006)001234567890120000(21)ABCDEFGHIJKLMNOP/RST",
        "tag_uri": "urn:epc:tag:itip-212:0.012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST",
        "hex": "41000B7F7070D40000830A1C48B1A3C8932A5CC9B3A7D05F4A9D4000",
    },
    {
        "scheme": PGLN,
        "tag_encodable": False,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:pgln:0123456789.01",
        "gs1_key": "0123456789012",
        "gs1_element_string": "(417)0123456789012",
        "company_prefix_length": 10,
    },
    {
        "scheme": SGCN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgcn:401234512345..1",
        "gs1_key": "40123451234561",
        "gs1_element_string": "(255)40123451234561",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:sgcn-96:7.401234512345..1",
        "hex": "3FE175ADC32764000000000B",
    },
    {
        "scheme": SGLN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgln:061411123456..A%2F-BCDEFGHIJKLMNOPQR",
        "gs1_key": "0614111234560",
        "gs1_element_string": "(414)0614111234560(254)A/-BCDEFGHIJKLMNOPQR",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:sgln-195:0.061411123456..A%2F-BCDEFGHIJKLMNOPQR",
        "hex": "390039318D8401057AD850E2458D1E449952E64D9D3E851A4000",
    },
    {
        "scheme": SGTIN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
        "gs1_key": "00000095010939",
        "gs1_element_string": "(01)00000095010939(21)Serial",
        "company_prefix_length": 8,
        "tag_uri": "urn:epc:tag:sgtin-198:2.00000950.01093.Serial",
        "hex": "36500001DB011169E5E5A70EC000000000000000000000000000",
    },
    {
        "scheme": SGTIN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
        "gs1_key": "0000095010939",
        "gs1_element_string": "(01)00000095010939(21)Serial",
        "company_prefix_length": 8,
        "tag_uri": "urn:epc:tag:sgtin-198:2.00000950.01093.Serial",
        "hex": "36500001DB011169E5E5A70EC000000000000000000000000000",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
    },
    {
        "scheme": SGTIN,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sgtin:00000950.01093.Serial",
        "gs1_key": "95010939",
        "gs1_element_string": "(01)00000095010939(21)Serial",
        "company_prefix_length": 8,
        "tag_uri": "urn:epc:tag:sgtin-198:2.00000950.01093.Serial",
        "hex": "36500001DB011169E5E5A70EC000000000000000000000000000",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
    },
    {
        "scheme": SSCC,
        "tag_encodable": True,
        "gs1_keyed": True,
        "gs1_element": True,
        "uri": "urn:epc:id:sscc:061414123456.12345",
        "gs1_key": "106141412345623458",
        "gs1_element_string": "(00)106141412345623458",
        "company_prefix_length": 12,
        "tag_uri": "urn:epc:tag:sscc-96:0.061414123456.12345",
        "hex": "31003932449F003039000000",
    },
    {
        "scheme": UPUI,
        "tag_encodable": False,
        "gs1_keyed": False,
        "gs1_element": True,
        "uri": "urn:epc:id:upui:1234567.089456.51qIgY)%3C%26Jp3*j7'SDB",
        "gs1_element_string": "(01)01234567894560(235)51qIgY)<&Jp3*j7'SDB",
    },
    {
        "scheme": USDOD,
        "tag_encodable": True,
        "gs1_keyed": False,
        "gs1_element": False,
        "uri": "urn:epc:id:usdod:2S194.68719476735",
        "tag_uri": "urn:epc:tag:usdod-96:15.2S194.68719476735",
        "hex": "2FF203253313934FFFFFFFFF",
    },
]


class TestParsersValid(unittest.TestCase):
    def test_epc_pure_identity_to_scheme(self):
        for epc in VALID_TEST_DATA:
            expected_scheme = epc["scheme"].from_epc_uri(epc["uri"])
            actual_scheme = epc_pure_identity_to_scheme(epc["uri"])

            self.assertEqual(expected_scheme, actual_scheme)

    def test_epc_pure_identity_to_gs1_element(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_element"]:
                expected_scheme = epc["scheme"].from_epc_uri(epc["uri"])
                actual_scheme = epc_pure_identity_to_gs1_element(epc["uri"])

                self.assertEqual(expected_scheme, actual_scheme)

    def test_epc_pure_identity_to_gs1_element_string(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_element"]:
                actual_gs1_element_string = epc_pure_identity_to_gs1_element_string(
                    epc["uri"]
                )

                self.assertEqual(epc["gs1_element_string"], actual_gs1_element_string)

    def test_epc_pure_identity_to_gs1_keyed(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"]:
                expected_scheme = epc["scheme"].from_epc_uri(epc["uri"])
                actual_scheme = epc_pure_identity_to_gs1_keyed(epc["uri"])

                self.assertEqual(expected_scheme, actual_scheme)

    def test_epc_pure_identity_to_gs1_key(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"]:
                actual_gs1_key = epc_pure_identity_to_gs1_key(
                    epc["uri"], **epc["kwargs"] if "kwargs" in epc else {}
                )

                self.assertEqual(epc["gs1_key"], actual_gs1_key)

    def test_epc_pure_identity_to_tag_encodable(self):
        for epc in VALID_TEST_DATA:
            if epc["tag_encodable"]:
                expected_scheme = epc["scheme"].from_epc_uri(epc["uri"])
                actual_scheme = epc_pure_identity_to_tag_encodable(epc["uri"])

                self.assertEqual(expected_scheme, actual_scheme)

    def test_tag_uri_to_tag_encodable(self):
        for epc in VALID_TEST_DATA:
            if epc["tag_encodable"]:
                expected_scheme = epc["scheme"].from_epc_uri(epc["uri"])
                actual_scheme = tag_uri_to_tag_encodable(epc["tag_uri"])

                self.assertEqual(expected_scheme, actual_scheme)

    def test_hex_to_tag_encodable(self):
        for epc in VALID_TEST_DATA:
            if epc["tag_encodable"]:
                expected_scheme = epc["scheme"].from_epc_uri(epc["uri"])
                actual_scheme = hex_to_tag_encodable(epc["hex"])

                self.assertEqual(expected_scheme, actual_scheme)


class TestParsersInvalid(unittest.TestCase):
    def test_invalid_epc_pure_identity_to_gs1_element(self):
        with self.assertRaises(ConvertException):
            epc_pure_identity_to_gs1_element("urn:epc:id:adi:W81X9C.3KL984PX1.2WMA-52")

    def test_invalid_epc_pure_identity_to_gs1_element_string(self):
        with self.assertRaises(ConvertException):
            epc_pure_identity_to_gs1_element_string("urn:epc:id:bic:CSQJ3054381")

    def test_invalid_epc_pure_identity_to_gs1_key(self):
        with self.assertRaises(ConvertException):
            epc_pure_identity_to_gs1_key(
                "urn:epc:id:itip:012345678901.0.00.00.ABCDEFGHIJKLMNOP%2FRST"
            )

    def test_invalid_epc_pure_identity_to_gs1_keyed(self):
        with self.assertRaises(ConvertException):
            epc_pure_identity_to_gs1_keyed(
                "urn:epc:id:upui:1234567.089456.51qIgY)%3C%26Jp3*j7'SDB"
            )

    def test_invalid_epc_pure_identity_to_scheme(self):
        with self.assertRaises(ConvertException):
            epc_pure_identity_to_scheme("urn:epc:id:dod:2S194.68719476735")

    def test_invalid_epc_pure_identity_to_tag_encodable(self):
        with self.assertRaises(ConvertException):
            epc_pure_identity_to_tag_encodable("urn:epc:id:pgln:0123456789.01")

    def test_invalid_hex_to_tag_encodable(self):
        with self.assertRaises(ConvertException):
            hex_to_tag_encodable("3AFFFFFFFFFFFFFFFFFFFFFF")

    def test_invalid_tag_uri_to_tag_encodable(self):
        with self.assertRaises(ConvertException):
            tag_uri_to_tag_encodable("urn:epc:tag:imovn-96:0.9176187")


class TestGS1KeyParser(unittest.TestCase):
    def test_source_epc_uri(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"]:
                actual_gs1_key = get_gs1_key(
                    epc["uri"], **epc["kwargs"] if "kwargs" in epc else {}
                )

                self.assertEqual(epc["gs1_key"], actual_gs1_key)

    def test_source_gs1_element_string(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"]:
                actual_gs1_key = get_gs1_key(
                    epc["gs1_element_string"],
                    company_prefix_length=epc["company_prefix_length"],
                    **epc["kwargs"] if "kwargs" in epc else {}
                )

                self.assertEqual(epc["gs1_key"], actual_gs1_key)

    def test_source_tag_uri(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"] and epc["tag_encodable"]:
                actual_gs1_key = get_gs1_key(
                    epc["tag_uri"], **epc["kwargs"] if "kwargs" in epc else {}
                )

                self.assertEqual(epc["gs1_key"], actual_gs1_key)

    def test_source_idpat(self):
        for epc in VALID_ID_PATTERNS:
            actual_gs1_key = get_gs1_key(
                epc["idpat"], **epc["kwargs"] if "kwargs" in epc else {}
            )

            self.assertEqual(epc["gs1_key"], actual_gs1_key)


VALID_ID_PATTERNS = [
    {
        "scheme": GDTI,
        "idpat": "urn:epc:idpat:gdti:0614141.12345.*",
        "gs1_key": "0614141123452*",
    },
    {
        "scheme": GIAI,
        "idpat": "urn:epc:idpat:giai:0614141.*",
        "gs1_key": "0614141*",
    },
    {
        "scheme": GINC,
        "idpat": "urn:epc:idpat:ginc:061411.*",
        "gs1_key": "061411*",
    },
    {
        "scheme": GRAI,
        "idpat": "urn:epc:idpat:grai:0614141.12345.*",
        "gs1_key": "0614141123452*",
    },
    {
        "scheme": GSIN,
        "idpat": "urn:epc:idpat:gsin:061414.0123456789",
        "gs1_key": "06141401234567891",
    },
    {
        "scheme": GSRN,
        "idpat": "urn:epc:idpat:gsrn:012345678901.01234",
        "gs1_key": "012345678901012342",
    },
    {
        "scheme": GSRNP,
        "idpat": "urn:epc:idpat:gsrnp:012345678901.01234",
        "gs1_key": "012345678901012342",
    },
    {
        "scheme": PGLN,
        "idpat": "urn:epc:idpat:pgln:0123456789.01",
        "gs1_key": "0123456789012",
    },
    {
        "scheme": SGCN,
        "idpat": "urn:epc:idpat:sgcn:401234512345..1",
        "gs1_key": "40123451234561",
    },
    {
        "scheme": SGLN,
        "idpat": "urn:epc:idpat:sgln:061411123456..*",
        "gs1_key": "0614111234560",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.01093.*",
        "gs1_key": "00000095010939",
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.01093.*",
        "gs1_key": "0000095010939",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN13},
    },
    {
        "scheme": SGTIN,
        "idpat": "urn:epc:idpat:sgtin:00000950.01093.*",
        "gs1_key": "95010939",
        "kwargs": {"gtin_type": GTIN_TYPE.GTIN8},
    },
    {
        "scheme": SSCC,
        "idpat": "urn:epc:idpat:sscc:061414123456.12345",
        "gs1_key": "106141412345623458",
    },
]
