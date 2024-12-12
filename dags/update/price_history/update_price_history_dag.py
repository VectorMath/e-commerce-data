"""
DAG for update price history in our database.

The DAG have the following pipeline:
- Waiting for execution of DAG that add new products in our database;
- Getting URLs of price history from products in our database;
- For every URL parse price history;
- Upload new data in current table 'price_history' in our database;
- Clear XCOM cache;
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config, global_dag_task
from dags.update.price_history import update_price_history_dag_config as dag_config
from dags.update.price_history import update_price_history_dag_task as dag_task

from src import config
from src.database.postgres import postgres_db_constant

# Define the DAG
with DAG(
        dag_id=global_dag_config.UPDATE_PRICE_HISTORY_TABLE_DAG_ID,
        schedule_interval=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["schedule_interval"],
        max_active_runs=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["max_active_runs"],
        tags=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["tags"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
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
    get_price_urls_from_table_urls_task = PythonOperator(
        task_id=dag_config.GET_PRICE_URLS_FROM_TABLE_URLS_TASK_ID,
        python_callable=dag_task.get_price_urls_from_table_urls,
        provide_context=True
    )

    find_update_for_prices_task = PythonOperator(
        task_id=dag_config.FIND_UPDATE_FOR_PRICES_TASK_ID,
        python_callable=dag_task.find_update_for_prices,
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
            global_dag_config.XCOM_DAG_ID_COLUMN: global_dag_config.UPDATE_PRICE_HISTORY_TABLE_DAG_ID
        }
    )

    sort_rows_in_table_task = PythonOperator(
        task_id=global_dag_config.SORT_DATA_IN_TABLE_TASK_ID,
        python_callable=global_dag_task.sort_data_in_table,
        op_kwargs={
            "table_name": config.PRICE_HISTORY_TABLE,
            "index": postgres_db_constant.INDEX_PRICE_HISTORY
        }
    )

    """Setting up a tasks sequence
    """
    wait_for_add_products_sensor >> get_price_urls_from_table_urls_task
    get_price_urls_from_table_urls_task >> find_update_for_prices_task
    find_update_for_prices_task >> upload_updated_data_to_table_task
    upload_updated_data_to_table_task >> sort_rows_in_table_task >> clear_xcom_cache_task
