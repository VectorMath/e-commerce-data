import unittest
from unittest.mock import patch, MagicMock

import psycopg2

from src.database.postgres.ConnectorPostgres import ConnectorPostgres


class TestConnectorPostgres(unittest.TestCase):

    @patch("psycopg2.connect")
    def test_create_connection_success(self, mock: MagicMock):
        mock_connection = MagicMock()
        mock.return_value = mock_connection
        host = "test_localhost"
        database = "test_db"
        user = "test_username"
        password = "test_password"

        postgres_connector = ConnectorPostgres(host, database, user, password)

        mock.assert_called_once_with(host=host, database=database, user=user, password=password)
        self.assertEqual(postgres_connector.get_connection(), mock_connection)
        self.assertEqual(postgres_connector.get_cursor(), mock_connection.cursor())

    @patch("psycopg2.connect")
    def test_create_connection_Connection_Error(self, mock: MagicMock):
        mock.side_effect = psycopg2.errors.ConnectionException
        with self.assertRaises(psycopg2.errors.ConnectionException):
            ConnectorPostgres()

    @patch("src.database.postgres.ConnectorPostgres.ConnectorPostgres.create_connection")
    def test_create_connection_Operational_Error(self, mock: MagicMock):
        mock.side_effect = psycopg2.errors.OperationalError()
        with self.assertRaises(psycopg2.errors.OperationalError):
            ConnectorPostgres()


if __name__ == '__main__':
    unittest.main()
