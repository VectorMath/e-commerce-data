"""
Here contains constants values and common functions
for DAG-files 'create_price_table_dag.py' and 'create_price_table_dag_task.py'
"""
from airflow.utils.dates import days_ago

from src import config
from src.database.postgres import postgres_db_constant

"""IDs for DAG and tasks."""
DAG_ID = "create-price-table"
WAIT_FOR_UPDATE_PRICE_HISTORY_SENSOR_ID = "wait_for_update_price_history"
DROP_TABLE_PRICE_TASK_ID = "drop_table_price"
CREATE_TABLE_PRICE_TASK_ID = "create_table_price"
CLOSE_CONNECTION_TASK_ID = "close_connection"

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

ALTER TABLE {config.PRICE_TABLE}
ADD CONSTRAINT fk_product_id
FOREIGN KEY ({postgres_db_constant.PRODUCT_ID})
REFERENCES public.{config.PRODUCT_TABLE}({postgres_db_constant.PRODUCT_ID})
ON DELETE CASCADE;
"""
