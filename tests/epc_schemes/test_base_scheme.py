import unittest
from typing import Any, Dict, List

from epcpy.epc_schemes.base_scheme import EPCScheme, GS1Keyed, TagEncodable
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
                    self.assertEqual(scheme.from_epc_uri(epc_uri).epc_uri, epc_uri)
                except ConvertException:
                    self.fail(
                        f"{scheme} init unexpectedly raised ConvertException for URI {epc_uri}"
                    )

            return test

        def generate_invalid_init_tests(scheme: EPCScheme, epc_uri: str):
            def test(self: unittest.TestCase):
                with self.assertRaises(ConvertException):
                    scheme.from_epc_uri(epc_uri)

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
        def generate_valid_gs1_key_tests(
            scheme: EPCScheme, epc_uri: str, gs1_key: str, **kwargs
        ):
            def test(self: unittest.TestCase):
                s: GS1Keyed = scheme.from_epc_uri(epc_uri)
                try:
                    self.assertEqual(s.gs1_key(**kwargs), gs1_key)
                except ConvertException:
                    self.fail(
                        f"{scheme} GS1Key unexpectedly raised ConvertException for URI {epc_uri} and kwargs {kwargs}"
                    )

            return test

        def generate_valid_gs1_element_string_tests(
            scheme: EPCScheme, epc_uri: str, gs1_element_string: str, **kwargs
        ):
            def test(self: unittest.TestCase):
                s: GS1Keyed = scheme.from_epc_uri(epc_uri)
                try:
                    self.assertEqual(s.gs1_element_string(), gs1_element_string)
                except ConvertException:
                    self.fail(
                        f"{scheme} GS1 element string unexpectedly raised ConvertException for URI {epc_uri} and kwargs {kwargs}"
                    )

            return test

        def generate_valid_from_gs1_element_string_test(
            scheme: GS1Keyed, epc_uri: str, gs1_element_string: str
        ):
            def test(self: unittest.TestCase):
                try:
                    s: EPCScheme = scheme.from_gs1_element_string(gs1_element_string)
                    self.assertEqual(s.epc_uri, epc_uri)
                except ConvertException:
                    self.fail(
                        f"{scheme} from gs1 element string unexpectedly raised ConvertException for URI {epc_uri}"
                    )

            return test

        def generate_invalid_gs1_key_tests(scheme: EPCScheme, epc_uri: str, **kwargs):
            def test(self: unittest.TestCase):
                s: GS1Keyed = scheme.from_epc_uri(epc_uri)
                with self.assertRaises(ConvertException):
                    s.gs1_key(**kwargs)

            return test

        for entry in valid_data:
            attrs[entry["name"]] = generate_valid_gs1_key_tests(
                scheme,
                entry["uri"],
                entry["gs1_key"],
                **entry["kwargs"] if "kwargs" in entry else {},
            )

            attrs[entry["name"]] = generate_valid_gs1_element_string_tests(
                scheme,
                entry["uri"],
                entry["gs1_element_string"],
                **entry["kwargs"] if "kwargs" in entry else {},
            )

            # attrs[entry["name"]] = generate_valid_from_gs1_element_string_test(
            #     scheme,
            #     entry["uri"],
            #     entry["gs1_element_string"],
            #     **entry["kwargs"] if "kwargs" in entry else {},
            # )

        for entry in invalid_data:
            attrs[entry["name"]] = generate_invalid_gs1_key_tests(
                scheme, entry["uri"], **entry["kwargs"] if "kwargs" in entry else {}
            )

        return type.__new__(cls, name, bases, attrs)


class TestTagEncodableMeta(type):
    def __new__(
        cls,
        name,
        bases,
        attrs,
        scheme: EPCScheme = None,
        valid_data: List[Dict[str, Any]] = None,
        invalid_data: List[Dict[str, Any]] = None,
    ):
        def generate_valid_to_tag_uri_test(
            scheme: EPCScheme, epc_uri: str, tag_uri: str, **kwargs
        ):
            def test(self: unittest.TestCase):
                s: TagEncodable = scheme.from_epc_uri(epc_uri)
                try:
                    self.assertEqual(s.tag_uri(**kwargs), tag_uri)
                except ConvertException:
                    self.fail(
                        f"{scheme} tag uri unexpectedly raised ConvertException for URI {epc_uri} and kwargs {kwargs}"
                    )

            return test

        def generate_valid_to_hex_test(
            scheme: EPCScheme, epc_uri: str, hex_string: str, **kwargs
        ):
            def test(self: unittest.TestCase):
                s: TagEncodable = scheme.from_epc_uri(epc_uri)
                try:
                    self.assertEqual(s.hex(**kwargs), hex_string)
                except ConvertException:
                    self.fail(
                        f"{scheme} hex unexpectedly raised ConvertException for URI {epc_uri} and kwargs {kwargs}"
                    )

            return test

        def generate_valid_from_tag_uri_test(
            scheme: TagEncodable, epc_uri: str, tag_uri: str
        ):
            def test(self: unittest.TestCase):
                try:
                    s: EPCScheme = scheme.from_tag_uri(tag_uri)
                    self.assertEqual(s.epc_uri, epc_uri)
                except ConvertException:
                    self.fail(
                        f"{scheme} from tag uri unexpectedly raised ConvertException for URI {epc_uri}"
                    )

            return test

        def generate_valid_from_hex_test(
            scheme: TagEncodable, epc_uri: str, hex_string: str
        ):
            def test(self: unittest.TestCase):
                try:
                    s: EPCScheme = scheme.from_hex(hex_string)
                    self.assertEqual(s.epc_uri, epc_uri)
                except ConvertException:
                    self.fail(
                        f"{scheme} from hex unexpectedly raised ConvertException for URI {epc_uri}"
                    )

            return test

        def generate_invalid_tag_encodable_tests(
            scheme: EPCScheme, epc_uri: str, **kwargs
        ):
            def test(self: unittest.TestCase):
                s: TagEncodable = scheme.from_epc_uri(epc_uri)
                with self.assertRaises(ConvertException):
                    s.tag_uri(**kwargs)

            return test

        for entry in valid_data:
            name = entry["name"]
            attrs[f"{name}_to_tag_uri"] = generate_valid_to_tag_uri_test(
                scheme,
                entry["uri"],
                entry["tag_uri"],
                **entry["kwargs"] if "kwargs" in entry else {},
            )
            attrs[f"{name}_from_tag_uri"] = generate_valid_from_tag_uri_test(
                scheme,
                entry["uri"],
                entry["tag_uri"],
            )
            attrs[f"{name}_to_hex"] = generate_valid_to_hex_test(
                scheme,
                entry["uri"],
                entry["hex"],
                **entry["kwargs"] if "kwargs" in entry else {},
            )
            attrs[f"{name}_from_hex"] = generate_valid_from_hex_test(
                scheme,
                entry["uri"],
                entry["hex"],
            )

        for entry in invalid_data:
            attrs[entry["name"]] = generate_invalid_tag_encodable_tests(
                scheme, entry["uri"], **entry["kwargs"] if "kwargs" in entry else {}
            )

        return type.__new__(cls, name, bases, attrs)
