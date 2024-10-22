from typing import Any

import pandas as pd

import constants
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
        pass

    def find_key_in_dict(self, dictionary: dict, target_key: str) -> str:
        """Method that searching specific key in dictionary and return value
        :param dictionary: required dict
        :param target_key: key that need to find
        :return: value from dictionary[target_key]
        """
        if not isinstance(dictionary, dict):
            return config.NULL_VALUE

        if target_key in dictionary:
            return dictionary[target_key]

        for key, value in dictionary.items():
            if isinstance(value, dict):
                found_value: Any = self.find_key_in_dict(value, target_key)
                if found_value is not config.NULL_VALUE:
                    return found_value

        return config.NULL_VALUE

    def get_table_size(self) -> str:
        """ Method that get table size value
        :return: string of table size
        """
        tech_sizes: list[str] = []
        sizes_table = self._data.get(constants.PRODUCT_SIZES_TABLE, {})
        values = sizes_table.get(constants.PRODUCT_DETAIL_KEY_VALUE, [])

        for item in values:
            tech_size = item.get(constants.PRODUCT_SIZES_TABLE_TECH_SIZE_KEY)
            if tech_size:
                tech_sizes.append(tech_size)

        return constants.SPLIT_VALUE.join(tech_sizes)

    def get_characteristic_from_options(self, name_type: str) -> str:
        """Method that extract characteristic values from options-key
        :param name_type: type of characteristic
        :return:  value in string format
        """
        characteristics: list[dict] = self._data.get(constants.PRODUCT_DETAIL_LIST_KEY, [])

        for item in characteristics:
            if item.get(constants.NAME_KEY) == name_type:
                return item.get(constants.PRODUCT_DETAIL_KEY_VALUE, '')

        return config.NULL_VALUE


print(pd.read_csv('csv/price-history.csv').shape)