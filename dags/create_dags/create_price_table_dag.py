"""
DAG for creating a table with the actual price for products.
Once completed, the table `price` will be populated with the most recent prices.
"""

from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator
from src import config
from src.database.postgres import postgres_db_constant
from src.database.postgres.ConnectorPostgres import ConnectorPostgres
from src.database.postgres.ClientPostgres import ClientPostgres

# Create an instance of the PostgreSQL client
client = ClientPostgres(ConnectorPostgres())

# Default arguments for the DAG
DEFAULT_ARGS = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

# SQL queries
DROP_PRICE_TABLE_QUERY = f"""DROP TABLE IF EXISTS {config.PRICE_TABLE};"""

CREATE_PRICE_TABLE_QUERY = f"""
CREATE TABLE {config.PRICE_TABLE} AS (
    SELECT {postgres_db_constant.PRODUCT_ID},
           {postgres_db_constant.DATE},
           {postgres_db_constant.PRICE}
    FROM (
        SELECT *,
               ROW_NUMBER() OVER (
                    PARTITION BY {postgres_db_constant.PRODUCT_ID}
                    ORDER BY {postgres_db_constant.DATE} DESC
               ) AS row_num
        FROM public.{config.PRICE_HISTORY_TABLE}
    ) AS sub_query
    WHERE row_num = 1
);
"""


# Python callback functions to execute SQL queries
def drop_price_table_if_exists():
    """Drops the existing price table if it exists.
    """
    client.execute_sql(query=DROP_PRICE_TABLE_QUERY, is_return=False)


def create_price_table_from_history():
    """Creates the price table with the latest prices for each product.
    """
    client.execute_sql(query=CREATE_PRICE_TABLE_QUERY, is_return=False)


def close_postgres_connection():
    """Closes the PostgreSQL connection.
    """
    client.close_connection()


# Define the DAG
with DAG(
        dag_id="create-price-table",
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["create"],
        default_args=DEFAULT_ARGS
) as dag:
    # Task 1: Drop the existing price table
    drop_price_table_task = PythonOperator(
        task_id="drop_price_table",
        python_callable=drop_price_table_if_exists
    )

    # Task 2: Create the price table
    create_price_table_task = PythonOperator(
        task_id="create_price_table",
        python_callable=create_price_table_from_history
    )

    # Task 3: Close the connection to the PostgreSQL database
    close_connection_task = PythonOperator(
        task_id="close_connection",
        python_callable=close_postgres_connection
    )

    # Define task dependencies
    drop_price_table_task >> create_price_table_task >> close_connection_task
