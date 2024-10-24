from typing import Any

from . import constants # "import constants" get error in tests.
from src import config


class ParserDictWB:
    """Class that make work of extracting data from dictionary.
    Using in ParserWB.
    """

    def __init__(self, data: dict):
        """Class constructor
        :param data: the dictionary that need to be extract
        """
        self._data: dict = data

    def find_key_in_dict(self, target_key: str) -> str:
        """Method that searching specific key in dictionary and return value
        :param target_key: key that need to find
        :return: value from dictionary[target_key]
        """
        if not isinstance(self._data, dict):
            return config.NULL_VALUE

        if target_key in self._data:
            return self._data[target_key]

        return config.NULL_VALUE

    def get_table_size(self) -> str:
        """ Method that get table size value
        :return: string of table size
        """
        sizes: list[str] = []
        sizes_table = self._data.get(constants.PRODUCT_SIZES_TABLE, {})
        values = sizes_table.get(constants.PRODUCT_DETAIL_KEY_VALUES, [])

        for item in values:
            details = item.get(constants.PRODUCT_SIZE_DETAILS)
            if details:
                sizes.append(details[0])

        def extract_min_value(size):
            """For case when we have size like 42-48
            """
            if '-' in size:
                return int(size.split('-')[0])
            return int(size)

        sizes = sorted(sizes, key=extract_min_value)
        return constants.SPLIT_VALUE.join(sizes)

    def get_characteristic_from_options(self, name_type: Any) -> str:
        """Method that extract characteristic values from options-key
        :param name_type: type of characteristic
        :return:  value in string format
        """
        characteristics: list[dict] = self._data.get(constants.PRODUCT_DETAIL_LIST_KEY, [])

        for item in characteristics:
            if item.get(constants.NAME_KEY) in name_type:
                return item.get(constants.PRODUCT_DETAIL_KEY_VALUE, '')

        return config.NULL_VALUE
