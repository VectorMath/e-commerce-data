import unittest

from src.parser.WB import constants

from src import config
from src.parser.WB.ProductDictExtractWB import ProductDictExtractWB
import test_data


class TestProductDictExtractWB(unittest.TestCase):
    """Test class for ParserDictWB
    """

    def setUp(self):
        self.data = test_data.product_response

    def test_get_table_size(self):
        """Test method of get_table_size from ParserDictWB.
        """
        self.assertEqual(ProductDictExtractWB.get_table_size(self.data), test_data.actual_sizes)

    def test_get_characteristic_from_options(self):
        """Test method of get_characteristic_from_options from ParserDictWB.
        """
        self.assertEqual(ProductDictExtractWB.get_characteristic_from_options(self.data,
                                                                      constants.PRODUCT_DETAIL_MADE_IN),
                         test_data.actual_made_in_value)
        self.assertEqual(ProductDictExtractWB.get_characteristic_from_options(self.data,
                                                                      constants.PRODUCT_DETAIL_COLOR),
                         test_data.actual_color)
        self.assertEqual(ProductDictExtractWB.get_characteristic_from_options(self.data,
                                                                      constants.PRODUCT_DETAIL_COMPOSITIONS),
                         test_data.actual_compositions)
        self.assertEqual(ProductDictExtractWB.get_characteristic_from_options(self.data,
                                                                      test_data.non_existed_key),
                         config.NULL_VALUE)


if __name__ == '__main__':
    unittest.main()
