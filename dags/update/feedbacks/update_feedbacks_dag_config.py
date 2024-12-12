"""
Here contains constants values and common functions
for DAG-files 'update_feedbacks_dag.py' and 'update_feedbacks_dag_task.py'
"""
from datetime import datetime

from airflow.utils.dates import days_ago

from dags import global_dag_config
from src import config
from src.database.postgres import postgres_db_constant

DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

"""Names for tmp tables.
"""
CURRENT_DATE: str = datetime.now().strftime('%Y_%m_%d')
TMP_FEEDBACKS_TABLE_NAME: str = f"update_tmp_feedbacks_{CURRENT_DATE}"

"""IDs for DAG and tasks."""
WAIT_FOR_ADD_PRODUCTS_SENSOR_ID: str = "wait_for_add_products"
GET_ROOT_AND_PRODUCT_IDS_FROM_TABLE_PRODUCTS_TASK_ID: str = "get_root_and_product_ids_from_table_products"
FIND_UPDATE_FOR_FEEDBACKS_TASK_ID: str = "find_update_for_feedbacks"
UPLOAD_UPDATED_DATA_TO_TABLE_TASK_ID: str = "upload_updated_data_to_table"
SORT_DATA_IN_FEEDBACKS_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID+f"_{config.FEEDBACKS_TABLE}"


"""SQL queries"""
SELECT_IDS_FROM_TABLE_PRODUCTS_QUERY: str = f"""
SELECT {postgres_db_constant.ROOT_ID}, {postgres_db_constant.PRODUCT_ID} 
FROM {config.PRODUCT_TABLE};
"""
