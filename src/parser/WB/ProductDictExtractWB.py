from typing import Any

from src.parser.WB import constants
from src import config


class ProductDictExtractWB:
    """Static class that make work of extracting data from dictionary.
    Using in method parse_product of class ParserWB.
    """

    def __new__(cls, *args, **kwargs):
        """In case if someone want to create object of this class
        """
        raise TypeError("Unable to create static class")

    @staticmethod
    def get_table_size(data: dict) -> str:
        """ Method that get table size value
        :param data: response dictionary
        :return: string of table size
        """
        sizes: list[str] = []
        sizes_table = data.get(constants.PRODUCT_SIZES_TABLE, config.NULL_VALUE)

        if sizes_table is not config.NULL_VALUE:
            values = sizes_table.get(constants.PRODUCT_DETAIL_KEY_VALUES, config.NULL_VALUE)
        else:
            return config.NULL_VALUE

        for item in values:
            details = item.get(constants.PRODUCT_SIZE_DETAILS)
            if details:
                sizes.append(details[0])

        def extract_min_value(size):
            """For case when we have size like 42-48 or 1/2, or 18,5
            """
            if '-' in size:
                return int(size.split('-')[0])
            elif '/' in size:
                return int(size.split('/')[0])
            elif ',' in size:
                return int(size.split(',')[0])
            return int(size)

        sizes = sorted(sizes, key=extract_min_value)
        return constants.SPLIT_VALUE.join(sizes)

    @staticmethod
    def get_characteristic_from_options(data: dict, name_type: Any) -> str:
        """Method that extract characteristic values from options-key
        :param data: response dictionary
        :param name_type: type of characteristic
        :return:  value in string format
        """
        characteristics: list[dict] = data.get(constants.PRODUCT_DETAIL_LIST_KEY, config.NULL_VALUE)

        if characteristics is not config.NULL_VALUE:
            for item in characteristics:
                if item.get(constants.NAME_KEY) in name_type:
                    return item.get(constants.PRODUCT_DETAIL_KEY_VALUE, config.NULL_VALUE)
        else:
            return config.NULL_VALUE
