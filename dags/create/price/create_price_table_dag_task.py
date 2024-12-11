"""
File that contain functional of DAG-tasks.
"""
from dags.create.price import create_price_table_dag_config as dag_config
from dags.global_dag_config import client

# Python callback functions to execute SQL queries
def drop_price_table_if_exists():
    """Drops the existing price table if it exists.
    """
    client.execute_sql(query=dag_config.DROP_PRICE_TABLE_QUERY, is_return=False)


def create_price_table_from_history():
    """Creates the price table with the latest prices for each product.
    """
    client.execute_sql(query=dag_config.CREATE_PRICE_TABLE_QUERY, is_return=False)
