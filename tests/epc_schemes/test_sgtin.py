import unittest
from epcpy.epc_schemes.sgtin import *
from epcpy.utils.parsers import binary_to_epc_tag_uri, binary_to_epc_pure_identity

class TestSGTINScheme(unittest.TestCase):

    def test_sgtin_to_gs1(self):
        sgtin = SGTIN("urn:epc:id:sgtin:00000950.01093.Serial")
        self.assertEqual(sgtin.gs1_element_string(), '(01)00000095010939(21)Serial')
        self.assertEqual(sgtin.gs1_key(), '00000095010939')
        self.assertEqual(sgtin.gtin(gtin=GTIN.GTIN8), '95010939')

    def test_sgtin_to_tag(self):
        sgtin = SGTIN("urn:epc:id:sgtin:00000950.01093.Serial")
        self.assertEqual(sgtin.tag_uri(BinaryCodingSchemes.SGTIN_198, SGTINFilterValues.POS_ITEM), 'urn:epc:tag:sgtin-198:1.00000950.01093.Serial')
        self.assertEqual(sgtin.hex(), '36300001DB011169E5E5A70EC000000000000000000000000000')

    def test_tag_to_sgtin(self):
        sgtin = SGTIN("urn:epc:id:sgtin:00000950.01093.Serial")
        sgtin.tag_uri(BinaryCodingSchemes.SGTIN_198, SGTINFilterValues.POS_ITEM)
        sgtin_binary = sgtin.binary()
        self.assertEqual(binary_to_epc_tag_uri(sgtin_binary), 'urn:epc:tag:sgtin-198:1.00000950.01093.Serial')
        self.assertEqual(binary_to_epc_pure_identity(sgtin_binary), 'urn:epc:id:sgtin:00000950.01093.Serial')

if __name__ == '__main__':
    unittest.main()
