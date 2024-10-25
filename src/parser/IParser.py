import pandas as pd


class IParser:
    """The parser interface
    """

    def parse_product_list(self, page_number: int) -> pd.DataFrame:
        """Get ID list of products from current page

        :return: dataframe with ids
        """
        pass

    def parse_product_personal_info(self, product_url: str) -> pd.DataFrame:
        """Get info personal info about product with current product_id

        :param product_url: url of product
        :return: Data frame with info about product
        """
        pass

    def parse_product_price_history(self, price_url: str) -> pd.DataFrame:
        """Get price history of current product

        :param price_url: url of price history
        :return: json response
        """
        pass

    def parse_product_feedback(self, product_id: int, root_id: int) -> pd.DataFrame:
        """Get feedback of product by root_id, by scrapping data, using selenium

        :param product_id: id of product
        :param root_id: id section of product
        :return: feedback table
        """
        pass
