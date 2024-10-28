import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock

import pandas as pd
import pandas.testing as pdt
import requests.exceptions

from src.parser.IParser import IParser
from src.parser.WB import constants
from src.parser.WB.ParserWB import ParserWB
from tests.parser.WB import test_data


class TestParserWB(unittest.TestCase):
    def setUp(self):
        self.parser: IParser = ParserWB()

    @patch(test_data.mock_method)
    def test_parse_product_list(self, mock: MagicMock):
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

    @patch(test_data.mock_method)
    def test_parse_product_list_HTTP_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.parser.parse_product_list(1)

    @patch(test_data.mock_method)
    def test_parse_product_list_Connection_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.parser.parse_product_list(1)

    @patch(test_data.mock_method)
    def test_parse_product_list_Key_Error(self, mock: MagicMock):
        product_dict_with_invalid_key = {
            test_data.non_existed_key: 1,
            constants.ROOT_KEY: 2,
            constants.NAME_KEY: "Test1"
        }
        mock.return_value.json.return_value = {
            constants.DATA_KEY: {constants.PRODUCTS_KEY: [product_dict_with_invalid_key]}}
        mock.side_effect = KeyError
        with self.assertRaises(KeyError):
            self.parser.parse_product_list(1)

    @patch(test_data.mock_method)
    def test_parse_product_personal_info(self, mock: MagicMock):
        mock.return_value.json.return_value = test_data.product_response
        actual_product_info = {
            constants.PRODUCT_ID: str(test_data.product_response["nm_id"]),
            constants.PRODUCT_DESCRIPTION: test_data.product_response[constants.PRODUCT_DESCRIPTION],
            constants.PRODUCT_CATEGORY: test_data.product_response[constants.PRODUCT_CATEGORY],
            constants.PRODUCT_MAIN_CATEGORY: test_data.product_response[constants.PRODUCT_MAIN_CATEGORY],
            constants.PRODUCT_BRAND_NAME: "Nordics",
            constants.PRODUCT_SIZES_TABLE: "42, 44, 46, 48, 50, 52, 54, 56, 58",
            constants.PRODUCT_MIN_SIZE: "42",
            constants.PRODUCT_MAX_SIZE: "58",
            constants.PRODUCT_COLOR: "черный",
            constants.PRODUCT_MADE_IN: "Китай",
            constants.PRODUCT_COMPOSITIONS: "флис; полиэстер; эластан",
            constants.DATE: datetime.now().strftime("%Y-%m-%d")
        }
        actual_result = pd.DataFrame([actual_product_info])
        pdt.assert_frame_equal(self.parser.parse_product_personal_info(
            "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/info/ru/card.json"), actual_result)

    @patch(test_data.mock_method)
    def test_parse_product_personal_info_HTTP_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.parser.parse_product_personal_info(
                "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/info/ru/card.json")

    @patch(test_data.mock_method)
    def test_parse_product_personal_info_Connection_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.parser.parse_product_personal_info(
                "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/info/ru/card.json")

    @patch(test_data.mock_method)
    def test_parse_product_personal_info_Key_Error(self, mock: MagicMock):
        product_dict_with_invalid_key = {
            "imt_id": 227510481,
            "nm_id": 251750385,
            "imt_name": "Термобелье комплект зимний спортивный",
            "slug": "termobele-komplekt-zimnij-sportivnyj",
            "subj_name": "Термокомплекты",
            test_data.non_existed_key: "Белье"
        }
        mock.return_value = product_dict_with_invalid_key
        mock.side_effect = KeyError
        with self.assertRaises(KeyError):
            self.parser.parse_product_personal_info(
                "https://basket-16.wbbasket.ru/vol2517/part251750/251750385/info/ru/card.json")

    @patch(test_data.mock_method)
    def test_parse_product_personal_info_Index_Error(self, mock: MagicMock):
        mock.side_effect = IndexError
        with self.assertRaises(IndexError):
            self.parser.parse_product_personal_info("invalid_url")

    @patch(test_data.mock_method)
    def test_parse_product_price_history(self, mock: MagicMock):
        mock.return_value.json.return_value = test_data.price_history_response

        actual_price_history_df = pd.DataFrame({
            constants.PRODUCT_ID: [test_data.product_id] * len(test_data.price_history_response),
            constants.DATE: pd.to_datetime(["2024-09-15", "2024-09-22"]),
            constants.PRICE_HISTORY_PRICE_KEY: [3210.75, 2463.6]
        })

        pdt.assert_frame_equal(self.parser.parse_product_price_history(test_data.price_history_url),
                               actual_price_history_df)

    @patch(test_data.mock_method)
    def test_parse_product_price_history_HTTP_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.parser.parse_product_price_history(test_data.price_history_url)

    @patch(test_data.mock_method)
    def test_parse_product_price_history_Connection_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.parser.parse_product_price_history(test_data.price_history_url)

    @patch(test_data.mock_method)
    def test_parse_product_price_history_Key_Error(self, mock: MagicMock):
        mock.return_value.json.return_value = [{test_data.non_existed_key: 1}, {test_data.non_existed_key: 2}]

        mock.side_effect = KeyError
        with self.assertRaises(KeyError):
            self.parser.parse_product_price_history(test_data.price_history_url)

    @patch(test_data.mock_method)
    def test_parse_product_price_history_Index_Error(self, mock: MagicMock):
        mock.return_value.json.return_value = test_data.price_history_response

        mock.side_effect = IndexError
        with self.assertRaises(IndexError):
            self.parser.parse_product_price_history(test_data.price_history_url_with_index_error)

    @patch(test_data.mock_method)
    def test_parse_product_feedback(self, mock: MagicMock):
        mock.return_value.json.return_value = test_data.feedback_response

        actual_feedback_df = pd.DataFrame(test_data.feedback_ready_dict)
        pdt.assert_frame_equal(self.parser.parse_product_feedback(251750385, 227510481),
                               actual_feedback_df)

    @patch(test_data.mock_method)
    def test_parse_product_feedback_HTTP_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.HTTPError
        with self.assertRaises(requests.exceptions.HTTPError):
            self.parser.parse_product_feedback(251750385, 227510481)

    @patch(test_data.mock_method)
    def test_parse_product_feedback_Connection_Error(self, mock: MagicMock):
        mock.side_effect = requests.exceptions.ConnectionError
        with self.assertRaises(requests.exceptions.ConnectionError):
            self.parser.parse_product_feedback(251750385, 227510481)

    @patch(test_data.mock_method)
    def test_parse_product_feedback_Key_Error(self, mock: MagicMock):
        mock.return_value.json.return_value = test_data.feedback_response_with_invalid_key

        mock.side_effect = KeyError
        with self.assertRaises(KeyError):
            self.parser.parse_product_feedback(251750385, 227510481)


if __name__ == '__main__':
    unittest.main()
