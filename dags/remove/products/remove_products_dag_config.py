"""
Here contains constants values and common functions
for DAG-files 'remove_products_dag.py' and 'remove_products_dag_task.py'
"""
from airflow.utils.dates import days_ago

from src import config

"""IDs for DAG and tasks."""
DAG_ID = "remove-products"
FIND_PRODUCTS_WITH_BAD_RESPONSE_CODE_TASK_ID = "check_response_from_products_url"
REMOVE_PRODUCTS_FROM_DATABASE_TASK_ID = "remove_products_from_database"
CLEAR_XCOM_CACHE_TASK_ID = "clear_xcom_cache"
CLOSE_CONNECTION_TASK_ID = "close_connection"

DEFAULT_ARGS = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

SELECT_ALL_DATA_FROM_TABLE_URLS_QUERY = f"""
SELECT * FROM {config.URLS_TABLE};
"""

DELETE_XCOM_CACHE_QUERY: str = f"""
DELETE FROM airflow.xcom
WHERE dag_id = '{DAG_ID}';
"""