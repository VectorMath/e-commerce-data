"""
Here contains constants values and common functions
for DAG-files 'update_price_history_dag.py' and 'update_price_history_dag_task.py'
"""
from datetime import datetime

from airflow.utils.dates import days_ago

from src import config
from src.database.postgres import postgres_db_constant

"""IDs for DAG and tasks."""
WAIT_FOR_ADD_PRODUCTS_SENSOR_ID: str = "wait_for_add_products"
GET_PRICE_URLS_FROM_TABLE_URLS_TASK_ID: str = "get_price_urls_from_table_urls"
FIND_UPDATE_FOR_PRICES_TASK_ID: str = "find_update_for_prices"
UPLOAD_UPDATED_DATA_TO_TABLE_TASK_ID: str = "upload_updated_data_to_table"
CLEAR_XCOM_CACHE_TASK_ID: str = "clear_xcom_cache"
CLOSE_CONNECTION_TASK_ID: str = "close_connection"

# Default arguments for DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

"""Names for tmp tables.
"""
CURRENT_DATE: str = datetime.now().strftime('%Y_%m_%d')
TMP_PRICE_HISTORY_TABLE_NAME: str = f"update_tmp_price_history_{CURRENT_DATE}"

"""SQL queries
"""
SELECT_PRICE_URLS_FROM_TABLE_PRICE_HISTORY_QUERY: str = f"""
SELECT {postgres_db_constant.PRODUCT_PRICE_HISTORY_JSON} FROM {config.URLS_TABLE};
"""
