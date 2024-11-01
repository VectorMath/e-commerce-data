import unittest

import requests

from src.parser.WB.ResponseValidatorWB import ResponseValidatorWB
from tests.parser.WB import test_data


class TestResponseValidatorWB(unittest.TestCase):

    def test_validate_product_list_id(self):
        response = test_data.product_id_list_response
        self.assertEqual(ResponseValidatorWB.validate_product_list_id(response), True)

    def test_validate_product(self):
        response = test_data.product_response
        self.assertEqual(ResponseValidatorWB.validate_product(response), True)

    def test_validate_price_history(self):
        response = test_data.price_history_response
        self.assertEqual(ResponseValidatorWB.validate_price_history(response), True)

    def test_validate_feedback(self):
        response = test_data.feedback_response
        self.assertEqual(ResponseValidatorWB.validate_feedback(response), True)

    """Tests with KeyError
    """
    def test_validate_product_list_id_with_invalid_key(self):
        with self.assertRaises(KeyError):
            ResponseValidatorWB.validate_product_list_id(test_data.product_id_list_response_with_invalid_key)

    def test_validate_product_with_invalid_key(self):
        with self.assertRaises(KeyError):
            ResponseValidatorWB.validate_product(test_data.product_response_with_invalid_key)

    def test_validate_price_history_with_invalid_key(self):
        with self.assertRaises(KeyError):
            ResponseValidatorWB.validate_price_history(test_data.price_history_response_with_invalid_key)

    def test_validate_feedback_with_invalid_key(self):
        with self.assertRaises(KeyError):
            ResponseValidatorWB.validate_feedback(test_data.feedback_response_with_invalid_key)

    """Network tests, checking real actual structure of responses.
    """

    def test_validate_product_list_id_network(self):
        response = requests.get(test_data.product_id_list_url).json()
        self.assertEqual(ResponseValidatorWB.validate_product_list_id(response), True)

    def test_validate_product_network(self):
        response = requests.get(test_data.product_url).json()
        self.assertEqual(ResponseValidatorWB.validate_product(response), True)

    def test_validate_price_history_network(self):
        response = requests.get(test_data.price_history_url).json()
        self.assertEqual(ResponseValidatorWB.validate_price_history(response), True)

    def test_validate_feedback_network(self):
        response = requests.get(test_data.feedback_url).json()
        self.assertEqual(ResponseValidatorWB.validate_feedback(response), True)


if __name__ == '__main__':
    unittest.main()
