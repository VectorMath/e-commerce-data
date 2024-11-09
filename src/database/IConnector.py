from typing import Any


class IConnector:
    """The connection interface.
    """

    def create_connection(self, *args) -> Any:
        """Method that creating connection to database
        :param args: different parameters that which are implementation dependent
        """
        pass

    def close_connection(self):
        """Method that close connection to database.
        """
        pass