"""
Here contains constants values and common functions
for DAG-files 'remove_products_dag.py' and 'remove_products_dag_task.py'
"""
from airflow.utils.dates import days_ago

from src import config

"""IDs for DAG and tasks."""
FIND_PRODUCTS_WITH_BAD_RESPONSE_CODE_TASK_ID: str = "check_response_from_products_url"
REMOVE_PRODUCTS_FROM_DATABASE_TASK_ID: str = "remove_products_from_database"

DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

SELECT_ALL_DATA_FROM_TABLE_URLS_QUERY: str = f"""
SELECT * FROM {config.URLS_TABLE};
"""
