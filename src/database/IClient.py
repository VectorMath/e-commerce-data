import pandas


class IClient:
    def execute_sql(self, query: str):
        pass

    def create_dataframe_by_sql(self, query: str) -> pandas.DataFrame:
        pass

    def create_table_in_db_by_sql(self, query: str, table_name: str):
        pass

    def create_table_in_db_by_df(self, df: pandas.DataFrame, table_name: str):
        pass

    def update_table_in_db_by_sql(self, query: str, table_name: str):
        pass

    def update_table_in_db_by_df(self, df: pandas.DataFrame, table_name: str):
        pass