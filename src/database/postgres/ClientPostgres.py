import pandas

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
        self.get_connector().get_connection().close()
        self.get_connector().get_cursor().close()

    def execute_sql(self, query: str, is_return: bool):
        """Realization of method execute_sql from interface IClient.
        """
        self.get_connector().get_cursor().execute(query)
        if is_return:
            return self.get_connector().get_cursor().fetchall()
        else:
            self.get_connector().get_connection().commit()

    def create_dataframe_by_sql(self, query: str) -> pandas.DataFrame:
        """Realization of method create_dataframe_by_sql from interface IClient.
        """
        data = self.execute_sql(query, True)
        return pandas.DataFrame(data,
                                columns=[desc[0] for desc in self.get_connector().get_cursor().description])

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
            self.get_connector().get_cursor().execute(insert_query, row)

        self.get_connector().get_connection().commit()

    def update_table_in_db_by_df(self,
                                 df: pandas.DataFrame,
                                 table_name: str,
                                 data_type: dict):
        """Realization of method update_table_in_db_by_df from interface IClient.
        """
        self.create_table_in_db_by_df(df, postgres_db_constant.TMP_TABLE, data_type)

        sql_where_cases = ' AND '.join(
            [f"{table_name}.{column} = {postgres_db_constant.TMP_TABLE}.{column}"
             for column in list(data_type.keys())])

        query = f'''
        INSERT INTO {table_name} 
        SELECT * FROM {postgres_db_constant.TMP_TABLE}
        WHERE NOT EXISTS (
            SELECT 1
            FROM {table_name}
            WHERE {sql_where_cases}
        );
        '''
        self.get_connector().get_cursor().execute(query)
        self.get_connector().get_connection().commit()
        self.execute_sql(f"DROP TABLE IS EXISTS {postgres_db_constant.TMP_TABLE}", False)

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