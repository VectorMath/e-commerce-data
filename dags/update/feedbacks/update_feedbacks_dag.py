"""
DAG for updating data in table 'feedbacks', that already exist.

The DAG have the following pipeline:
- Waiting for execution of DAG that add new products in our database;
- Getting root and product IDs from products in our database;
- For every couple root_id and product_id parse feedback;
- Upload new data in current table 'feedbacks' in our database;
- Clear XCOM cache;
- Close connection;
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config, global_dag_task
from dags.update.feedbacks import update_feedbacks_dag_config as dag_config
from dags.update.feedbacks import update_feedbacks_dag_task as dag_task
from src import config
from src.database.postgres import postgres_db_constant

with DAG(
        dag_id=global_dag_config.UPDATE_FEEDBACKS_TABLE_DAG_ID,
        schedule_interval=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["schedule_interval"],
        max_active_runs=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["max_active_runs"],
        tags=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["tags"],
        default_args=dag_config.DEFAULT_ARGS
):
    """Define sensor
    """
    wait_for_add_products_sensor = ExternalTaskSensor(
        task_id=dag_config.WAIT_FOR_ADD_PRODUCTS_SENSOR_ID,
        external_dag_id=global_dag_config.ADD_PRODUCT_IN_TABLE_DAG_ID,
        external_task_id=global_dag_config.DEFAULT_SENSORS_PARAMETERS["external_task_id"],
        poke_interval=global_dag_config.DEFAULT_SENSORS_PARAMETERS["poke_interval"],
        timeout=global_dag_config.DEFAULT_SENSORS_PARAMETERS["timeout"]
    )

    """Define tasks
    """
    get_root_and_product_ids_from_table_products_task = PythonOperator(
        task_id=dag_config.GET_ROOT_AND_PRODUCT_IDS_FROM_TABLE_PRODUCTS_TASK_ID,
        python_callable=dag_task.get_root_and_product_ids_from_table_products,
        provide_context=True
    )

    find_update_for_feedbacks_task = PythonOperator(
        task_id=dag_config.FIND_UPDATE_FOR_FEEDBACKS_TASK_ID,
        python_callable=dag_task.find_update_for_feedbacks,
        provide_context=True
    )

    upload_updated_data_to_table_task = PythonOperator(
        task_id=dag_config.UPLOAD_UPDATED_DATA_TO_TABLE_TASK_ID,
        python_callable=dag_task.upload_updated_data_to_table,
        provide_context=True
    )

    clear_xcom_cache_task = PythonOperator(
        task_id=global_dag_config.CLEAR_XCOM_CACHE_TASK_ID,
        python_callable=global_dag_task.clear_xcom_cache,
        op_kwargs={
            global_dag_config.XCOM_DAG_ID_COLUMN: global_dag_config.UPDATE_FEEDBACKS_TABLE_DAG_ID
        }
    )

    sort_data_in_feedbacks_task = PythonOperator(
        task_id=dag_config.SORT_DATA_IN_FEEDBACKS_TASK_ID,
        python_callable=global_dag_task.sort_data_in_table,
        op_kwargs={
            "table_name": config.FEEDBACKS_TABLE,
            "index": postgres_db_constant.INDEX_FEEDBACKS
        }
    )

    """Setting up a tasks sequence
    """
    wait_for_add_products_sensor >> get_root_and_product_ids_from_table_products_task
    get_root_and_product_ids_from_table_products_task >> find_update_for_feedbacks_task
    find_update_for_feedbacks_task >> upload_updated_data_to_table_task
    upload_updated_data_to_table_task >> clear_xcom_cache_task
    clear_xcom_cache_task >> sort_data_in_feedbacks_task
