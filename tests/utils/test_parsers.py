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
from epcpy.utils.common import ConvertException
from tests.utils.test_data import (
    INVALID_ID_PATTERNS,
    VALID_ID_PATTERNS,
    VALID_TEST_DATA,
)


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

    def test_source_hex(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"] and epc["tag_encodable"]:
                actual_gs1_key = get_gs1_key(
                    epc["hex"], **epc["kwargs"] if "kwargs" in epc else {}
                )

                self.assertEqual(epc["gs1_key"], actual_gs1_key)

    def test_source_binary(self):
        for epc in VALID_TEST_DATA:
            if epc["gs1_keyed"] and epc["tag_encodable"]:
                actual_gs1_key = get_gs1_key(
                    epc["binary"], **epc["kwargs"] if "kwargs" in epc else {}
                )

                self.assertEqual(epc["gs1_key"], actual_gs1_key)

    def test_source_invalid_idpat(self):
        for epc in INVALID_ID_PATTERNS:
            with self.assertRaises(ConvertException):
                get_gs1_key(epc["idpat"], **epc["kwargs"] if "kwargs" in epc else {})
