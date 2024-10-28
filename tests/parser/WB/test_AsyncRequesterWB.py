import unittest
from unittest.mock import patch, MagicMock

import pandas as pd
import pandas.testing as pdt

from src.parser.WB.AsyncRequesterWB import AsyncRequesterWB
from tests.parser.WB import test_data
from src.parser.WB import constants


class TestAsyncRequesterWB(unittest.TestCase):
    def setUp(self):
        self.requester = AsyncRequesterWB(test_data.products_id_list,
                                          test_data.roots_id_list)

    @patch(test_data.mock_async_method)
    def test_create_table_with_json_urls(self, mock: MagicMock):
        mock.return_value = test_data.card_json_urls
        actual_df = pd.DataFrame({
            constants.PRODUCT_ID: self.requester.get_product_id_list(),
            constants.PRODUCT_CARD_JSON_TITLE: test_data.card_json_urls,
            constants.PRODUCT_PRICE_HISTORY_JSON_TITLE: test_data.price_history_json_urls
        })

        pdt.assert_frame_equal(self.requester.create_table_with_json_urls(), actual_df)

    @patch(test_data.mock_async_method)
    def test_create_table_with_json_urls_with_duplicate(self, mock: MagicMock):
        mock.return_value = test_data.card_json_urls_with_duplicate
        actual_df = pd.DataFrame({
            constants.PRODUCT_ID: self.requester.get_product_id_list(),
            constants.PRODUCT_CARD_JSON_TITLE: test_data.card_json_urls,
            constants.PRODUCT_PRICE_HISTORY_JSON_TITLE: test_data.price_history_json_urls
        })

        pdt.assert_frame_equal(self.requester.create_table_with_json_urls(), actual_df)


if __name__ == '__main__':
    unittest.main()
