from typing import Any


class IConnector:
    """The connection interface.
    """

    def create_connection(self, *args) -> Any:
        """"""
        pass

    def close_connection(self):
        """"""
        pass