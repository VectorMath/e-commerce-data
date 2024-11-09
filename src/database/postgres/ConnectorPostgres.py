from psycopg2._psycopg import connection, cursor

from src import config
from src.database.IConnector import IConnector
import psycopg2


class ConnectorPostgres(IConnector):
    """Class-realization of Interface IConnector for database Postgresql.
    """

    def __init__(self,
                 host: str = config.POSTGRES_HOST,
                 db: str = config.POSTGRES_DB_NAME,
                 username: str = config.POSTGRES_USERNAME,
                 password: str = config.POSTGRES_PASSWORD):
        """Constructor for class ConnectorPostgres.
        :param host: host of database.
        :param db: name of your database in Postgres.
        :username: name of your user in Postgres db.
        :password: password to your Postgres db.
        """
        self._host: str = host
        self._db: str = db
        self._username: str = username
        self._password: str = password

        self._connection: connection = self.create_connection()
        self._cursor: cursor = self.get_connection().cursor()

    def create_connection(self):
        """Realization of method create_connection in interface IConnector.
        For realization is taken library psycopg2.
        """
        return psycopg2.connect(host=self.get_host(),
                                database=self.get_db(),
                                user=self.get_username(),
                                password=self.get_password())

    def close_connection(self):
        """Realization of method close_connection in interface IConnector.
        Here we are closing fields _connection and _cursor.
        """
        self.get_connection().close()
        self.get_cursor().close()

    """Get/Set methods for all fields in class ConnectorPostgres.
    """
    def get_host(self) -> str:
        return self._host

    def set_host(self, host: str):
        self._host = host

    def get_db(self) -> str:
        return self._db

    def set_db(self, db: str):
        self._db = db

    def get_username(self) -> str:
        return self._username

    def set_username(self, username: str):
        self._username = username

    def get_password(self) -> str:
        return self._password

    def set_password(self, password: str):
        self._password = password

    def get_connection(self) -> connection:
        return self._connection

    def set_connection(self, _connection: connection):
        self._connection = _connection

    def get_cursor(self) -> cursor:
        return self._cursor

    def set_cursor(self, _cursor: cursor):
        self._cursor = _cursor
