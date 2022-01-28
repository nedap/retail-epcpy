import unittest
from typing import Any, Dict, List

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed
from epcpy.utils.common import ConvertException


class TestEPCSchemeInitMeta(type):
    def __new__(
        cls,
        name,
        bases,
        attrs,
        scheme: EPCScheme = None,
        valid_data: List[Dict[str, Any]] = None,
        invalid_data: List[Dict[str, Any]] = None,
    ):
        def generate_valid_init_tests(scheme: EPCScheme, epc_uri: str):
            def test(self: unittest.TestCase):
                try:
                    self.assertEqual(scheme(epc_uri).epc_uri, epc_uri)
                except ConvertException:
                    self.fail(
                        f"{scheme} init unexpectedly raised ConvertException for URI {epc_uri}"
                    )

            return test

        def generate_invalid_init_tests(scheme: EPCScheme, epc_uri: str):
            def test(self: unittest.TestCase):
                with self.assertRaises(ConvertException):
                    scheme(epc_uri)

            return test

        for entry in valid_data:
            attrs[entry["name"]] = generate_valid_init_tests(scheme, entry["uri"])

        for entry in invalid_data:
            attrs[entry["name"]] = generate_invalid_init_tests(scheme, entry["uri"])

        return type.__new__(cls, name, bases, attrs)


class TestGS1KeyedMeta(type):
    def __new__(
        cls,
        name,
        bases,
        attrs,
        scheme: EPCScheme = None,
        valid_data: List[Dict[str, Any]] = None,
        invalid_data: List[Dict[str, Any]] = None,
    ):
        def generate_valid_init_tests(
            scheme: EPCScheme, epc_uri: str, gs1_key: str, **kwargs
        ):
            def test(self: unittest.TestCase):
                try:
                    s: GS1Keyed = scheme(epc_uri)
                    self.assertEqual(s.gs1_key(**kwargs), gs1_key)
                except ConvertException:
                    self.fail(
                        f"{scheme} init unexpectedly raised ConvertException for URI {epc_uri}"
                    )

            return test

        def generate_invalid_init_tests(scheme: EPCScheme, epc_uri: str, **kwargs):
            def test(self: unittest.TestCase):
                s: GS1Keyed = scheme(epc_uri)
                with self.assertRaises(ConvertException):
                    s.gs1_key(**kwargs)

            return test

        for entry in valid_data:
            attrs[entry["name"]] = generate_valid_init_tests(
                scheme, entry["uri"], entry["gs1_key"], **entry["kwargs"]
            )

        for entry in invalid_data:
            attrs[entry["name"]] = generate_invalid_init_tests(
                scheme, entry["uri"], **entry["kwargs"]
            )

        return type.__new__(cls, name, bases, attrs)
