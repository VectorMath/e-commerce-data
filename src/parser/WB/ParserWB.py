import time
from datetime import datetime

import pandas as pd
import requests
from requests import Response

import constants
from src import config
from src.parser.IParser import IParser
from src.parser.WB.ParserDictWB import ParserDictWB


class ParserWB(IParser):
    """The realization of IParser for online store 'WildBerries'
    """

    def __init__(self):
        """Class Constructor
        """
        pass

    def parse_product_list(self) -> pd.DataFrame:
        result_table: list = []
        try:
            for page_number in range(constants.FIRST_PAGE, constants.LAST_PAGE):
                if page_number % constants.PRODUCT_LIST_PAGE_NUMBER_FOR_SLEEP == 0:
                    time.sleep(constants.TIME_FOR_SLEEP)

                url: str = constants.PRODUCT_LIST_URL.replace(constants.SYMBOL_TO_REPLACE_FOR_PAGE_NUMBER_IN_URL,
                                                              str(page_number))
                response: Response = requests.get(url)
                data: dict = response.json()[constants.DATA_KEY][constants.PRODUCTS_KEY]

                for product in data:
                    if constants.ID_KEY in product:
                        product_info = {
                            constants.PRODUCT_ID: str(product[constants.ID_KEY]),
                            constants.ROOT_ID: str(product[constants.ROOT_KEY]),
                            constants.PRODUCT_NAME: product[constants.NAME_KEY],
                        }
                        result_table.append(product_info)

            return pd.DataFrame(result_table)

        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)

    def parse_product_personal_info(self, product_url: str) -> pd.DataFrame:
        product: dict = {}

        try:
            data: dict = requests.get(product_url).json()
            dict_parser: ParserDictWB = ParserDictWB(data)

            product[constants.PRODUCT_ID] = product_url.split('/')[-4]  # Extract product_id from url
            '''Non-nested data in dictionary
            '''
            for key in constants.PRODUCT_PERSONAL_INFO_KEYS:
                product[key] = dict_parser.find_key_in_dict(key)

            '''Nested data in dictionary
            '''
            # Brand
            product[constants.PRODUCT_BRAND_NAME] = dict_parser.find_key_in_dict(constants.PRODUCT_SELLING)[
                constants.PRODUCT_BRAND_NAME]

            # Size columns
            product[constants.PRODUCT_SIZES_TABLE] = dict_parser.get_table_size()
            product[constants.PRODUCT_MIN_SIZE] = product[constants.PRODUCT_SIZES_TABLE].split(
                constants.SPLIT_VALUE)[0]
            product[constants.PRODUCT_MAX_SIZE] = product[constants.PRODUCT_SIZES_TABLE].split(
                constants.SPLIT_VALUE)[-1]

            # Colors column
            product[constants.PRODUCT_COLOR] = dict_parser.get_characteristic_from_options(
                constants.PRODUCT_DETAIL_COLOR)

            # Made in column
            product[constants.PRODUCT_MADE_IN] = dict_parser.get_characteristic_from_options(
                constants.PRODUCT_DETAIL_MADE_IN)

            # Compositions column
            product[constants.PRODUCT_COMPOSITIONS] = dict_parser.get_characteristic_from_options(
                constants.PRODUCT_DETAIL_COMPOSITIONS)

            # Upload date
            product[constants.DATE] = datetime.now().strftime("%Y-%m-%d")

            '''Sex determination with webdriver, 
            because json don't have information about for what sex that product'''
            return pd.DataFrame([product])

        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)

    def parse_product_price_history(self, price_url: str) -> pd.DataFrame:
        dt_list: list[datetime] = []
        price_list: list[float] = []

        try:
            data = requests.get(price_url).json()
            if data is not config.NULL_VALUE:
                for item in data:
                    dt_list.append(pd.to_datetime(item[constants.PRICE_HISTORY_DATE_KEY], unit='s'))

                    '''Example: in json price 41580 - that's not 41 580 RUB/DOLL, that 415.80
                    '''
                    correct_price = item[constants.PRICE_HISTORY_PRICE_KEY][
                                        constants.PRICE_HISTORY_CURRENT_CURRENCY_KEY] / 100
                    price_list.append(correct_price)

                return pd.DataFrame(
                    {
                        # Take product_id from url
                        constants.PRODUCT_ID: [price_url.split('/')[-3]] * len(price_list),
                        constants.DATE: dt_list,
                        constants.PRICE_HISTORY_PRICE_KEY: price_list
                    }
                )
        except requests.exceptions.HTTPError as e:
            raise SystemExit(e)

    def parse_product_feedback(self, product_id: int, root_id: int) -> pd.DataFrame:
        comments: list[str] = []
        comments_date: list[str] = []
        grades: list[int] = []
        product_ids: list[str] = []
        root_ids: list[str] = []

        for url in constants.FEEDBACK_URLS:
            feedback_url = url.replace(str(constants.ROOT_ID), str(root_id))

            try:
                feedbacks = requests.get(feedback_url, timeout=30).json()[constants.FEEDBACKS_KEY]
                if feedbacks is config.NULL_VALUE:
                    continue
                else:
                    for feedback in feedbacks:
                        if product_id == str(feedback[constants.FEEDBACK_PRODUCT_ID_KEY]):
                            comments.append(feedback[constants.FEEDBACK_COMMENT_KEY])
                            date = feedback[constants.FEEDBACK_DATE_KEY][:constants.FEEDBACK_LAST_INDEX_OF_DATE_STR]
                            comments_date.append(date)
                            grades.append(feedback[constants.FEEDBACK_GRADE_KEY])
                            product_ids.append(str(product_id))
                            root_ids.append(str(root_id))

                    return pd.DataFrame({
                        constants.ROOT_ID: root_ids,
                        constants.PRODUCT_ID: product_ids,
                        constants.DATE: comments_date,
                        constants.FEEDBACK_COMMENT_TITLE: comments,
                        constants.FEEDBACK_GRADE_TITLE: grades
                    })

            except requests.exceptions.HTTPError as e:
                raise SystemExit(e)