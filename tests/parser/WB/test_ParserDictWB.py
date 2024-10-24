import unittest

import requests

from src.parser.WB import constants

from src import config
from src.parser.WB.ParserDictWB import ParserDictWB
import test_data


class TestParserDictWB(unittest.TestCase):
    """Test class for ParserDictWB
    """
    def setUp(self):
        self.parser_dict = ParserDictWB(test_data.dict_for_test_ParserDictWB)

        """For case if WB would change JSON structure again
        """
        self.parser_dict_network = ParserDictWB(requests.get(test_data.url).json())

    def test_find_key_in_dict(self):
        """Test method of find_key_in_dict from ParserDictWB.
        """
        self.assertEqual(self.parser_dict.find_key_in_dict(test_data.existed_key),
                         test_data.value_from_existed_key)
        self.assertEqual(self.parser_dict.find_key_in_dict(test_data.non_existed_key),
                         config.NULL_VALUE)

        self.assertEqual(self.parser_dict_network.find_key_in_dict(test_data.existed_key),
                         test_data.value_from_existed_key)
        self.assertEqual(self.parser_dict_network.find_key_in_dict(test_data.non_existed_key),
                         config.NULL_VALUE)

    def test_get_table_size(self):
        """Test method of get_table_size from ParserDictWB.
        """
        self.assertEqual(self.parser_dict.get_table_size(), test_data.actual_sizes)

        self.assertEqual(self.parser_dict_network.get_table_size(), test_data.actual_sizes)

    def test_get_characteristic_from_options(self):
        """Test method of get_characteristic_from_options from ParserDictWB.
        """
        self.assertEqual(self.parser_dict.get_characteristic_from_options(constants.PRODUCT_DETAIL_MADE_IN),
                         test_data.actual_made_in_value)
        self.assertEqual(self.parser_dict.get_characteristic_from_options(constants.PRODUCT_DETAIL_COLOR),
                         test_data.actual_color)
        self.assertEqual(self.parser_dict.get_characteristic_from_options(constants.PRODUCT_DETAIL_COMPOSITIONS),
                         test_data.actual_compositions)
        self.assertEqual(self.parser_dict.get_characteristic_from_options(test_data.non_existed_key),
                         config.NULL_VALUE)

        self.assertEqual(self.parser_dict_network.get_characteristic_from_options(constants.PRODUCT_DETAIL_MADE_IN),
                         test_data.actual_made_in_value)
        self.assertEqual(self.parser_dict_network.get_characteristic_from_options(constants.PRODUCT_DETAIL_COLOR),
                         test_data.actual_color)
        self.assertEqual(self.parser_dict_network.get_characteristic_from_options(constants.PRODUCT_DETAIL_COMPOSITIONS),
                         test_data.actual_compositions)
        self.assertEqual(self.parser_dict_network.get_characteristic_from_options(test_data.non_existed_key),
                         config.NULL_VALUE)


if __name__ == '__main__':
    unittest.main()
