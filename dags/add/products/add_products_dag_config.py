"""
Here contains constants values and common functions
for DAG-files 'add_products_dag.py' and 'add_products_dag_task.py'
"""
from datetime import datetime

from airflow.utils.dates import days_ago

# Default arguments for the DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

"""IDs for DAG and tasks."""
DAG_ID = "add-products"
WAIT_FOR_REMOVING_PRODUCTS_SENSOR_ID = "wait_for_removing_products"
PARSE_ID_FROM_PRODUCT_LIST_TASK_ID = "parse_id_from_product_list"
PARSE_URLS_OF_PRODUCTS_TASK_ID = "parse_urls_of_products"
PARSE_PRODUCTS_PERSONAL_INFO_TASK_ID = "parse_products_personal_info"
PARSE_PRICE_HISTORY_TASK_ID = "parse_price_history"
PARSE_FEEDBACKS_TASK_ID = "parse_feedbacks"
UPLOAD_NEW_DATA_IN_PRODUCTS_TASK_ID = "upload_new_data_in_products"
UPLOAD_NEW_DATA_IN_URLS_TASK_ID = "upload_new_data_in_urls"
UPLOAD_NEW_DATA_IN_PRICE_HISTORY_TASK_ID = "upload_new_data_in_price_history"
UPLOAD_NEW_DATA_IN_FEEDBACKS_TASK_ID = "upload_new_data_in_feedbacks"
CLEAR_XCOM_CACHE_TASK_ID = "clear_xcom_cache"
CLOSE_CONNECTION_TASK_ID = "close_connection"


""""""
CURRENT_DATE = datetime.now().strftime('%Y_%m_%d')
TMP_PRODUCT_TABLE_NAME = f"tmp_products_{CURRENT_DATE}"
TMP_URLS_TABLE_NAME = f"tmp_urls_{CURRENT_DATE}"
TMP_PRICE_HISTORY_TABLE_NAME = f"tmp_price_history_{CURRENT_DATE}"
TMP_FEEDBACKS_TABLE_NAME = f"tmp_feedbacks_{CURRENT_DATE}"

IS_BAD_INTERNET = True

"""SQL-queries"""
DELETE_XCOM_CACHE_QUERY: str = f"""
DELETE FROM airflow.xcom
WHERE dag_id = '{DAG_ID}';
"""