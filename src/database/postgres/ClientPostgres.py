from typing import Any

import pandas
import psycopg2.errors

from src.database.IClient import IClient
from src.database.postgres import postgres_db_constant
from src.database.postgres.ConnectorPostgres import ConnectorPostgres


class ClientPostgres(IClient):
    """Class-realization of interface IClient for database Postgres."""

    def __init__(self, connector: ConnectorPostgres):
        """Constructor for class ClientPostgres.
        :param connector: connector that realize interface IConnector.
        """
        self._connector: ConnectorPostgres = connector

    def close_connection(self):
        """Realization of method close_connection from interface IClient.
        """
        self._connector.close_connection()

    def execute_sql(self, query: str, is_return: bool):
        """Realization of method execute_sql from interface IClient.
        """
        try:
            self._connector.get_cursor().execute(query)
            if is_return:
                return self._connector.get_cursor().fetchall()
            else:
                self._connector.get_connection().commit()
        except psycopg2.errors.OperationalError as e:
            print(f"[{self.__class__.__name__}] Operational error: {str(e)}")
            raise e
        except psycopg2.errors.ProgrammingError as e:
            print(f"[{self.__class__.__name__}] Programming error: {str(e)}")
            raise e
        except psycopg2.IntegrityError as e:
            print(f"[{self.__class__.__name__}] Integrity error: {str(e)}")
            raise e

    def create_dataframe_by_sql(self, query: str) -> pandas.DataFrame:
        """Realization of method create_dataframe_by_sql from interface IClient.
        """
        try:
            self._connector.get_cursor().execute(query)
            data: Any = self._connector.get_cursor().fetchall()

            return pandas.DataFrame(data,
                                    columns=[desc[0] for desc in self._connector.get_cursor().description])
        except psycopg2.errors.OperationalError as e:
            print(f"[{self.__class__.__name__}] Operational error: {str(e)}")
            raise e
        except psycopg2.errors.ProgrammingError as e:
            print(f"[{self.__class__.__name__}] Programming error: {str(e)}")
            raise e
        except psycopg2.IntegrityError as e:
            print(f"[{self.__class__.__name__}] Integrity error: {str(e)}")
            raise e

    def create_table_in_db_by_df(self,
                                 df: pandas.DataFrame,
                                 table_name: str,
                                 data_type: dict):
        """Realization of method create_table_in_db_by_df from interface IClient.

        How he works:
        - Created empty table with name, that you wrote in parameter table_name;
        - After that we take dataframe that you wrote in parameter df and insert every row in df to table by loop
        """

        '''Create-part. Here we just create table without filling data.
        '''
        columns: list = []
        for column in df.columns:
            column_type = data_type[column]
            columns.append(f'"{column}" {column_type}')

        create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(columns)});"
        self._connector.get_cursor().execute(create_query)

        '''Part when we insert data from dataframe to our created table.
        '''
        insert_columns = ', '.join([f'"{col}"' for col in df.columns])
        placeholders = ', '.join(['%s'] * len(df.columns))
        insert_query = f"INSERT INTO {table_name} ({insert_columns}) VALUES ({placeholders})"

        for row in df.itertuples(index=False, name=None):
            self._connector.get_cursor().execute(insert_query, row)

        self._connector.get_connection().commit()

    def update_table_in_db_by_df(self,
                                 df: pandas.DataFrame,
                                 table_name: str,
                                 tmp_table_name: str,
                                 is_main_table: bool,
                                 data_type: dict):
        """Realization of method update_table_in_db_by_df from interface IClient.
        """
        self.create_table_in_db_by_df(df=df,
                                      table_name=tmp_table_name,
                                      data_type=data_type)

        sql_where_cases: str = ' AND '.join(
            [f"{table_name}.{column} = {tmp_table_name}.{column}"
             for column in list(data_type.keys())])

        if is_main_table:
            query = f'''
            INSERT INTO {table_name} 
            SELECT * FROM {tmp_table_name}
            ON CONFLICT ({postgres_db_constant.PRODUCT_ID}) 
            DO UPDATE SET
                {postgres_db_constant.PRODUCT_DESCRIPTION} = EXCLUDED.{postgres_db_constant.PRODUCT_DESCRIPTION},
                {postgres_db_constant.PRODUCT_BRAND_NAME} = EXCLUDED.{postgres_db_constant.PRODUCT_BRAND_NAME},
                {postgres_db_constant.PRODUCT_MAIN_CATEGORY} = EXCLUDED.{postgres_db_constant.PRODUCT_MAIN_CATEGORY},
                {postgres_db_constant.PRODUCT_CATEGORY} = EXCLUDED.{postgres_db_constant.PRODUCT_CATEGORY},
                {postgres_db_constant.PRODUCT_SIZES_TABLE} = EXCLUDED.{postgres_db_constant.PRODUCT_SIZES_TABLE},
                {postgres_db_constant.PRODUCT_MIN_SIZE} = EXCLUDED.{postgres_db_constant.PRODUCT_MIN_SIZE},
                {postgres_db_constant.PRODUCT_MAX_SIZE} = EXCLUDED.{postgres_db_constant.PRODUCT_MAX_SIZE},
                {postgres_db_constant.PRODUCT_COLOR} = EXCLUDED.{postgres_db_constant.PRODUCT_COLOR},
                {postgres_db_constant.PRODUCT_MADE_IN} = EXCLUDED.{postgres_db_constant.PRODUCT_MADE_IN},
                {postgres_db_constant.PRODUCT_COMPOSITIONS} = EXCLUDED.{postgres_db_constant.PRODUCT_COMPOSITIONS};
            '''
        else:
            query = f'''
            INSERT INTO {table_name} 
            SELECT * FROM {tmp_table_name}
            WHERE NOT EXISTS (
                SELECT 1
                FROM {table_name}
                WHERE {sql_where_cases}
            );
            '''
        self._connector.get_cursor().execute(query)
        self._connector.get_connection().commit()
        self.execute_sql(f"DROP TABLE IF EXISTS {tmp_table_name}", False)

    def get_connector(self) -> ConnectorPostgres:
        """Get-method of field _connector
        :return: current connector of example ClientPostgres.
        """
        return self._connector

    def set_connector(self, connector: ConnectorPostgres):
        """Set-method of field _connector
        :param connector: new ConnectorPostgres
        """
        self._connector = connector
