import pandas


class IClient:
    """The interface that simulate work of database client.
    """

    def close_connection(self):
        """Method that close all connections in field connector
        """
        pass

    def execute_sql(self,
                    query: str,
                    is_return: bool):
        """Method that execute SQL-query in DB. He has 2 options:
        1) Can return to you result of SQL-query;
        2) Just execute SQL query and commit that;
        The parameter is_return responsible for the option
        :param query: SQL query that will be delivered to database.
        :param is_return: value that determines what do after execution.
        """
        pass

    def create_dataframe_by_sql(self, query: str) -> pandas.DataFrame:
        """Method that create dataframe from library Pandas by executing SQL-query
        :param query: SQL query that will be delivered to database.
        :return: Dataframe that contain result of sql-query execution.
        """
        pass

    def create_table_in_db_by_df(self,
                                 df: pandas.DataFrame,
                                 table_name: str,
                                 data_type: dict):
        """Method that create table in your database by dataframe from library Pandas.
        :param df: Dataframe that contain data for future table.
        :param table_name: name of the table that you want to create in your database.
        :param data_type: The dictionary with columns and type of that columns in future table.
        """
        pass

    def update_table_in_db_by_df(self,
                                 df: pandas.DataFrame,
                                 table_name: str,
                                 tmp_table_name: str,
                                 data_type: dict):
        """Method that update existed table in your database by dataframe from library Pandas
        :param df: Dataframe that contain data for table, that need be updated.
        :param table_name: name of table that you want to update.
        :param tmp_table_name: name of tmp table that will be take data from df.
        :param data_type: The dictionary with columns and type of that columns in table that need to be updated.
        """
        pass
