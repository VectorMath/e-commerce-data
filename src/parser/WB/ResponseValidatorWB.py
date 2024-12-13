from src.parser.WB import constants


class ResponseValidatorWB:
    """Static class that validate structure of response from API 'Wildberries'.
    Using in methods of class ParserWB.
    """

    def __new__(cls, *args, **kwargs):
        """In case if someone want to create object of this class
        """
        raise TypeError("Unable to create static class")

    @staticmethod
    def validate_product_list_id(response: dict) -> bool:
        """Static method that validate json-structure
        for method parse_product_list_id of class ParserWB.

        :param response: response from request
        :return: True value if structure not changed.
        """
        try:
            if response[constants.DATA_KEY]:
                if response[constants.DATA_KEY][constants.PRODUCTS_KEY]:
                    for product in response[constants.DATA_KEY][constants.PRODUCTS_KEY]:
                        if product[constants.ID_KEY]:
                            return True
        except KeyError as e:
            print(constants.INVALID_RESPONSE_MESSAGE + str(e))
            raise

    @staticmethod
    def validate_product(response: dict) -> bool:
        """Static method that validate json-structure
        for method parse_product of class ParserWB.

        We check only non-nested keys, because response for product request is dynamic.
        So, sometimes we have required keys, sometimes don't.

        For example, we don't have a key size_table for product of category electronics.

        :param response: response from request
        :return: True value if structure not changed.
        """
        try:
            for key in constants.PRODUCT_PERSONAL_INFO_KEYS:
                if response[key]:
                    continue
            return True
        except KeyError as e:
            print(constants.INVALID_RESPONSE_MESSAGE + str(e))
            raise

    @staticmethod
    def validate_price_history(response: dict) -> bool:
        """Static method that validate json-structure
        for method parse_product_price_history of class ParserWB.

        :param response: response from request
        :return: True value if structure not changed.
        """
        try:
            for price in response:
                if price[constants.PRICE_HISTORY_DATE_KEY]:
                    if price[constants.PRICE_HISTORY_PRICE_KEY]:
                        if price[constants.PRICE_HISTORY_PRICE_KEY][constants.PRICE_HISTORY_CURRENT_CURRENCY_KEY]:
                            return True
        except KeyError as e:
            print(constants.INVALID_RESPONSE_MESSAGE + str(e))
            raise

    @staticmethod
    def validate_feedback(response: dict) -> bool:
        """Static method that validate json-structure
         for method parse_product_feedback of class ParserWB.

         :param response: response from request
         :return: True value if structure not changed.
         """
        try:
            if response[constants.FEEDBACKS_KEY]:
                for feedback in response[constants.FEEDBACKS_KEY]:
                    if feedback[constants.FEEDBACK_PRODUCT_ID_KEY]:
                        if feedback[constants.FEEDBACK_COMMENT_KEY]:
                            if feedback[constants.FEEDBACK_DATE_KEY]:
                                if feedback[constants.FEEDBACK_GRADE_KEY]:
                                    return True
        except KeyError as e:
            print(constants.INVALID_RESPONSE_MESSAGE + str(e))
            raise
