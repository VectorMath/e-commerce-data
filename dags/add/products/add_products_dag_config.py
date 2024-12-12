"""
Here contains constants values and common functions
for DAG-files 'add_products_dag.py' and 'add_products_dag_task.py'
"""
from airflow.utils.dates import days_ago

from src import config

from dags import global_dag_config

# Default arguments for the DAG
DEFAULT_ARGS: dict = {
    "start_date": days_ago(1),
    "owner": 'eugene',
    "poke_interval": 600
}

"""IDs for tasks
"""
WAIT_FOR_REMOVING_PRODUCTS_SENSOR_ID: str = "wait_for_removing_products"

PARSE_ID_FROM_PRODUCT_LIST_TASK_ID: str = "parse_id_from_product_list"
PARSE_URLS_OF_PRODUCTS_TASK_ID: str = "parse_urls_of_products"
PARSE_PRODUCTS_PERSONAL_INFO_TASK_ID: str = "parse_products_personal_info"
PARSE_PRICE_HISTORY_TASK_ID: str = "parse_price_history"
PARSE_FEEDBACKS_TASK_ID: str = "parse_feedbacks"

UPLOAD_NEW_DATA_IN_PRODUCTS_TASK_ID: str = "upload_new_data_in_products"
UPLOAD_NEW_DATA_IN_URLS_TASK_ID: str = "upload_new_data_in_urls"
UPLOAD_NEW_DATA_IN_PRICE_HISTORY_TASK_ID: str = "upload_new_data_in_price_history"
UPLOAD_NEW_DATA_IN_FEEDBACKS_TASK_ID: str = "upload_new_data_in_feedbacks"

SORT_DATA_IN_PRODUCTS_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID+f"_{config.PRODUCT_TABLE}"
SORT_DATA_IN_PRICE_HISTORY_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID+f"_{config.PRICE_HISTORY_TABLE}"
SORT_DATA_IN_URLS_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID+f"_{config.URLS_TABLE}"
SORT_DATA_IN_FEEDBACKS_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID+f"_{config.FEEDBACKS_TABLE}"

"""Names for TMP tables.
"""
TMP_PRODUCT_TABLE_NAME: str = f"tmp_products_{global_dag_config.CURRENT_DATE_YYYY_MM_DD}"
TMP_URLS_TABLE_NAME: str = f"tmp_urls_{global_dag_config.CURRENT_DATE_YYYY_MM_DD}"
TMP_PRICE_HISTORY_TABLE_NAME: str = f"tmp_price_history_{global_dag_config.CURRENT_DATE_YYYY_MM_DD}"
TMP_FEEDBACKS_TABLE_NAME: str = f"tmp_feedbacks_{global_dag_config.CURRENT_DATE_YYYY_MM_DD}"

"""Boolean value that using in task-method 'parse_urls_of_products'.
If it's True then method will be parse only part of IDs from previous task. 
"""
IS_BAD_INTERNET: bool = True

"""SQL-queries.
"""
DELETE_XCOM_CACHE_QUERY: str = f"""
DELETE FROM {global_dag_config.AIRFLOW_DB_SCHEMA}.{global_dag_config.XCOM_TABLE_NAME}
WHERE {global_dag_config.XCOM_DAG_ID_COLUMN} = '{global_dag_config.ADD_PRODUCT_IN_TABLE_DAG_ID}';
"""
