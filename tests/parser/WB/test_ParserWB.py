import unittest
from unittest.mock import patch

import pandas as pd
import pandas.testing as pdt

from src.parser.IParser import IParser
from src.parser.WB import constants
from src.parser.WB.ParserWB import ParserWB


class TestParserWB(unittest.TestCase):
    def setUp(self):
        self.parser: IParser = ParserWB()

    @patch('requests.get')
    def test_parse_product_list(self, mock):
        product_dict = {
            constants.ID_KEY: 1,
            constants.ROOT_KEY: 2,
            constants.NAME_KEY: "Test1"
        }
        mock.return_value.json.return_value = {constants.DATA_KEY: {constants.PRODUCTS_KEY: [product_dict]}}

        actual_row_product = {
            constants.PRODUCT_ID: "1",
            constants.ROOT_ID: "2",
            constants.PRODUCT_NAME: "Test1"}
        actual_df = pd.DataFrame([actual_row_product])

        pdt.assert_frame_equal(self.parser.parse_product_list(1), actual_df)

    @patch('requests.get')
    def test_parse_product_list_with_code_200(self, mock):
        mock.return_value.status_code = 200
        actual_empty_df = pd.DataFrame()
        pdt.assert_frame_equal(self.parser.parse_product_list(1), actual_empty_df)

if __name__ == '__main__':
    unittest.main()
