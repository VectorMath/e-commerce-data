"""
Here contains constants values and common functions
for DAG-files 'update_products_dag.py' and 'update_products_dag_task.py'
"""
from datetime import datetime

from airflow.utils.dates import days_ago

from dags import global_dag_config
from src import config
from src.database.postgres import postgres_db_constant

"""IDs for DAG and tasks."""
WAIT_FOR_ADD_PRODUCTS_SENSOR_ID: str = "wait_for_add_products"
GET_CARD_URLS_FROM_TABLE_URLS_TASK_ID: str = "get_card_urls_from_table_urls"
FIND_UPDATE_FOR_PRODUCTS_TASK_ID: str = "find_update_for_products"
UPLOAD_UPDATED_DATA_TO_TABLE_TASK_ID: str = "upload_updated_data_to_table"
SORT_DATA_IN_PRODUCTS_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID+f"_{config.PRODUCT_TABLE}"

# Default arguments for DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

"""Names for tmp tables.
"""
CURRENT_DATE: str = datetime.now().strftime('%Y_%m_%d')
TMP_PRODUCTS_TABLE_NAME: str = f"update_tmp_products_{CURRENT_DATE}"

"""SQL queries
"""
SELECT_CARD_URLS_FROM_TABLE_PRICE_HISTORY_QUERY = f"""
SELECT {postgres_db_constant.PRODUCT_CARD_JSON} FROM {config.URLS_TABLE};
"""
