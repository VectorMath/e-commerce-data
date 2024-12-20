from datetime import datetime

import pandas as pd
import requests

from src.parser.WB import constants
from src import config
from src.parser.IParser import IParser
from src.parser.WB.ProductDictExtractWB import ProductDictExtractWB
from src.parser.WB.ResponseValidatorWB import ResponseValidatorWB


class ParserWB(IParser):
    """The realization of IParser for online store 'WildBerries'
    """

    def parse_product_list_id(self, page_number: int) -> pd.DataFrame:
        result_table: list = []
        try:
            url: str = constants.PRODUCT_LIST_URL.replace(constants.SYMBOL_TO_REPLACE_FOR_PAGE_NUMBER_IN_URL,
                                                          str(page_number))
            response = requests.get(url).json()
            if ResponseValidatorWB.validate_product_list_id(response):
                data: dict = response[constants.DATA_KEY][constants.PRODUCTS_KEY]

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
            print(f"HTTP Error: {e}")
            raise  # raise need for unit tests
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            raise

    def parse_product(self, product_url: str) -> pd.DataFrame:
        product: dict = {}

        try:
            response = requests.get(product_url).json()
            if ResponseValidatorWB.validate_product(response):
                data: dict = response

                product[constants.PRODUCT_ID] = product_url.split('/')[-4]  # Extract product_id from url
                '''Non-nested data in dictionary
                '''
                for key in constants.PRODUCT_PERSONAL_INFO_KEYS:
                    product[key] = data.get(key, config.NULL_VALUE)

                '''Nested data in dictionary
                '''
                # Brand
                selling_dict = data.get(constants.PRODUCT_SELLING, config.NULL_VALUE)
                if selling_dict is not config.NULL_VALUE:
                    product[constants.PRODUCT_BRAND_NAME] = selling_dict.get(constants.PRODUCT_BRAND_NAME,
                                                                             config.NULL_VALUE)

                # Size columns
                product[constants.PRODUCT_SIZES_TABLE] = ProductDictExtractWB.get_table_size(data)
                if product[constants.PRODUCT_SIZES_TABLE] is not config.NULL_VALUE:
                    product[constants.PRODUCT_MIN_SIZE] = product[constants.PRODUCT_SIZES_TABLE].split(
                        constants.SPLIT_VALUE)[0]
                    product[constants.PRODUCT_MAX_SIZE] = product[constants.PRODUCT_SIZES_TABLE].split(
                        constants.SPLIT_VALUE)[-1]
                else:
                    product[constants.PRODUCT_MIN_SIZE] = config.NULL_VALUE
                    product[constants.PRODUCT_MAX_SIZE] = config.NULL_VALUE

                # Colors column
                product[constants.PRODUCT_COLOR] = ProductDictExtractWB.get_characteristic_from_options(data,
                                                                                                        constants.PRODUCT_DETAIL_COLOR)

                # Made in column
                product[constants.PRODUCT_MADE_IN] = ProductDictExtractWB.get_characteristic_from_options(data,
                                                                                                          constants.PRODUCT_DETAIL_MADE_IN)

                # Compositions column
                product[constants.PRODUCT_COMPOSITIONS] = ProductDictExtractWB.get_characteristic_from_options(data,
                                                                                                               constants.PRODUCT_DETAIL_COMPOSITIONS)

                # Upload date
                product[constants.DATE] = datetime.now().strftime("%Y-%m-%d")

                product_df = pd.DataFrame([product])
                product_df.rename(columns={constants.PRODUCT_ROOT_ID: constants.ROOT_ID,
                                           constants.PRODUCT_NAME_KEY: constants.PRODUCT_NAME}, inplace=True)
                product_df = product_df[[
                    constants.ROOT_ID,
                    constants.PRODUCT_ID,
                    constants.DATE,
                    constants.PRODUCT_NAME,
                    constants.PRODUCT_DESCRIPTION,
                    constants.PRODUCT_BRAND_NAME,
                    constants.PRODUCT_MAIN_CATEGORY,
                    constants.PRODUCT_CATEGORY,
                    constants.PRODUCT_SIZES_TABLE,
                    constants.PRODUCT_MIN_SIZE,
                    constants.PRODUCT_MAX_SIZE,
                    constants.PRODUCT_COLOR,
                    constants.PRODUCT_MADE_IN,
                    constants.PRODUCT_COMPOSITIONS
                ]]
                return product_df

        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            raise
        except IndexError as e:
            print(f"Index Error: {e}")
            raise

    def parse_product_price_history(self, price_url: str) -> pd.DataFrame:
        dt_list: list[datetime] = []
        price_list: list[float] = []

        try:
            response = requests.get(price_url).json()
            if response is not config.NULL_VALUE:
                if ResponseValidatorWB.validate_price_history(response):
                    for item in response:
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
            print(f"HTTP Error: {e}")
            raise
        except requests.exceptions.ConnectionError as e:
            print(f"Connection Error: {e}")
            raise
        except IndexError as e:
            print(f"Index Error: {e}")
            raise

    def parse_product_feedback(self, product_id: int, root_id: int) -> pd.DataFrame:
        comments: list[str] = []
        comments_date: list[str] = []
        grades: list[int] = []
        product_ids: list[str] = []
        root_ids: list[str] = []

        for url in constants.FEEDBACK_URLS:
            feedback_url = url.replace(str(constants.ROOT_ID), str(root_id))

            try:
                response = requests.get(feedback_url, timeout=30).json()
                feedbacks = response[constants.FEEDBACKS_KEY]
                if feedbacks is config.NULL_VALUE:
                    continue
                else:
                    if ResponseValidatorWB.validate_feedback(response):
                        for feedback in feedbacks:
                            if str(product_id) == str(feedback[constants.FEEDBACK_PRODUCT_ID_KEY]):
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
                print(f"HTTP Error: {e}")
                raise
            except requests.exceptions.ConnectionError as e:
                print(f"Connection Error: {e}")
                raise
