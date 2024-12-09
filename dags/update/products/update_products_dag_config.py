"""
Here contains constants values and common functions
for DAG-files 'update_products_dag.py' and 'update_products_dag_task.py'
"""
from datetime import datetime

from airflow.utils.dates import days_ago

from src import config
from src.database.postgres import postgres_db_constant

"""IDs for DAG and tasks."""
DAG_ID = "update-products"
WAIT_FOR_ADD_PRODUCTS_SENSOR_ID = "wait_for_add_products"
GET_CARD_URLS_FROM_TABLE_URLS_TASK_ID = "get_card_urls_from_table_urls"
FIND_UPDATE_FOR_PRODUCTS_TASK_ID = "find_update_for_products"
UPLOAD_UPDATED_DATA_TO_TABLE_TASK_ID = "upload_updated_data_to_table"
CLEAR_XCOM_CACHE_TASK_ID = "clear_xcom_cache"
CLOSE_CONNECTION_TASK_ID = "close_connection"

# Default arguments for DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}


"""Names for tmp tables.
"""
CURRENT_DATE = datetime.now().strftime('%Y_%m_%d')
TMP_PRODUCTS_TABLE_NAME = f"update_tmp_products_{CURRENT_DATE}"

"""SQL queries
"""
SELECT_CARD_URLS_FROM_TABLE_PRICE_HISTORY_QUERY = f"""
SELECT {postgres_db_constant.PRODUCT_CARD_JSON} FROM {config.URLS_TABLE};
"""

DELETE_XCOM_CACHE_QUERY: str = f"""
DELETE FROM airflow.xcom
WHERE dag_id = '{DAG_ID}';
"""