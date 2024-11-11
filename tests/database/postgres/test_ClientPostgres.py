import unittest
from unittest.mock import MagicMock, patch

import pandas as pd
import psycopg2.errors

from src.database.postgres.ClientPostgres import ClientPostgres


class TestClientPostgres(unittest.TestCase):
    @patch('src.database.postgres.ConnectorPostgres')
    def setUp(self, mock_connector: MagicMock):
        self.mock_connector = mock_connector.return_value
        self.client = ClientPostgres(connector=self.mock_connector)

    def test_execute_sql_with_return_value(self):
        actual_result = [
            (1, 'value_of_col2', 'value_of_col3'),
            (2, 'value_of_col2', 'value_of_col3'),
            (3, 'value_of_col2', 'value_of_col3'),
        ]

        mock_connector: MagicMock = MagicMock()
        mock_cursor: MagicMock = MagicMock()
        mock_connector.get_cursor.return_value = mock_cursor
        mock_cursor.fetchall.return_value = actual_result

        client = ClientPostgres(connector=mock_connector)
        query = "SELECT * FROM some_table"
        result = client.execute_sql(query=query, is_return=True)

        mock_cursor.execute.assert_called_once_with(query)

        mock_cursor.fetchall.assert_called_once()

        self.assertEqual(result, actual_result)

    def test_execute_sql_without_return_value(self):
        mock_connector: MagicMock = MagicMock()
        mock_connection: MagicMock = MagicMock()
        mock_cursor: MagicMock = MagicMock()
        mock_connector.get_connection.return_value = mock_connection
        mock_connector.get_cursor.return_value = mock_cursor

        query = "SELECT * FROM some_table"
        ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=False)

        mock_cursor.execute.assert_called_once_with(query)
        mock_connection.commit.assert_called_once()

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres.get_cursor')
    def test_execute_sql_Operational_Error(self, mock_cursor: MagicMock):
        mock_connector: MagicMock = MagicMock()
        mock_connector.get_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.errors.OperationalError
        query = "SELECT * FROM some_table"

        with self.assertRaises(psycopg2.errors.OperationalError):
            ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=True)
            ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=False)

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres.get_cursor')
    def test_execute_sql_Programming_Error(self, mock_cursor: MagicMock):
        mock_connector: MagicMock = MagicMock()
        mock_connector.get_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.errors.ProgrammingError
        query = "SELECT * FROM some_table"

        with self.assertRaises(psycopg2.errors.ProgrammingError):
            ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=True)
            ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=False)

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres.get_cursor')
    def test_execute_sql_Integrity_Error(self, mock_cursor: MagicMock):
        mock_connector: MagicMock = MagicMock()
        mock_connector.get_cursor.return_value = mock_cursor
        mock_cursor.execute.side_effect = psycopg2.errors.IntegrityError
        query = "SELECT * FROM some_table"

        with self.assertRaises(psycopg2.errors.IntegrityError):
            ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=True)
            ClientPostgres(connector=mock_connector).execute_sql(query=query, is_return=False)

if __name__ == '__main__':
    unittest.main()
