"""
Here contains constants values and common functions
for DAG-files 'update_feedbacks_dag.py' and 'update_feedbacks_dag_task.py'
"""
from datetime import datetime

from airflow.utils.dates import days_ago

from src.database.postgres import postgres_db_constant
from src import config


DEFAULT_ARGS = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

"""Names for tmp tables.
"""
CURRENT_DATE = datetime.now().strftime('%Y_%m_%d')
TMP_FEEDBACKS_TABLE_NAME = f"update_tmp_feedbacks_{CURRENT_DATE}"


"""IDs for DAG and tasks."""
DAG_ID = "update-feedbacks"
WAIT_FOR_ADD_PRODUCTS_SENSOR_ID = "wait_for_add_products"
GET_ROOT_AND_PRODUCT_IDS_FROM_TABLE_PRODUCTS_TASK_ID = "get_root_and_product_ids_from_table_products"
FIND_UPDATE_FOR_FEEDBACKS_TASK_ID = "find_update_for_feedbacks"
UPLOAD_UPDATED_DATA_TO_TABLE_TASK_ID = "upload_updated_data_to_table"
CLEAR_XCOM_CACHE_TASK_ID = "clear_xcom_cache"
CLOSE_CONNECTION_TASK_ID = "close_connection"

"""SQL queries"""
SELECT_IDS_FROM_TABLE_PRODUCTS_QUERY = f"""
SELECT {postgres_db_constant.ROOT_ID}, {postgres_db_constant.PRODUCT_ID} 
FROM {config.PRODUCT_TABLE};
"""

DELETE_XCOM_CACHE_QUERY: str = f"""
DELETE FROM airflow.xcom
WHERE dag_id = '{DAG_ID}';
"""


