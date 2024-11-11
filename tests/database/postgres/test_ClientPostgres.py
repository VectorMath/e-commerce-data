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

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres')
    def test_create_dataframe_by_sql(self, mock_connector_postgres: MagicMock):
        mock_cursor = MagicMock()
        mock_cursor.fetchall.return_value = [(1, 'd')]
        mock_cursor.description = [('column1',), ('column2',)]

        mock_connector_postgres.get_cursor.return_value = mock_cursor

        expected_df = pd.DataFrame([(1, 'd')], columns=['column1', 'column2'])
        client = ClientPostgres(mock_connector_postgres)
        result_df = client.create_dataframe_by_sql("SELECT * FROM test")
        pd.testing.assert_frame_equal(result_df, expected_df)

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres')
    def test_create_dataframe_by_sql_Operational_Error(self, mock_connector_postgres: MagicMock):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg2.errors.OperationalError

        mock_connector_postgres.get_cursor.return_value = mock_cursor

        with self.assertRaises(psycopg2.errors.OperationalError):
            ClientPostgres(mock_connector_postgres).create_dataframe_by_sql("select * from test")

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres')
    def test_create_dataframe_by_sql_Programming_Error(self, mock_connector_postgres: MagicMock):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg2.errors.ProgrammingError

        mock_connector_postgres.get_cursor.return_value = mock_cursor

        with self.assertRaises(psycopg2.errors.ProgrammingError):
            ClientPostgres(mock_connector_postgres).create_dataframe_by_sql("select * from test")

    @patch('src.database.postgres.ConnectorPostgres.ConnectorPostgres')
    def test_create_dataframe_by_sql_Integrity_Error(self, mock_connector_postgres: MagicMock):
        mock_cursor = MagicMock()
        mock_cursor.execute.side_effect = psycopg2.errors.IntegrityError

        mock_connector_postgres.get_cursor.return_value = mock_cursor

        with self.assertRaises(psycopg2.errors.IntegrityError):
            ClientPostgres(mock_connector_postgres).create_dataframe_by_sql("select * from test")

if __name__ == '__main__':
    unittest.main()
