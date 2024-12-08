"""
DAG for update price history in our database.

The DAG have the following pipeline:
- Waiting for execution of DAG that add new products in our database;
- Getting URLs of price history from products in our database;
- For every URL parse price history;
- Upload new data in current table 'price_history' in our database;
- Clear XCOM cache;
- Close connection;
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config

from dags.update.price_history import update_price_history_dag_config as dag_config
from dags.update.price_history import update_price_history_dag_task as dag_task

# Define the DAG
with DAG(
        dag_id=dag_config.DAG_ID,
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["update"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
    """Define sensor
    """
    wait_for_add_products_sensor = ExternalTaskSensor(
        task_id=dag_config.WAIT_FOR_ADD_PRODUCTS_SENSOR_ID,
        external_dag_id=global_dag_config.UPDATE_PRICE_HISTORY_TABLE_DAG_ID,
        external_task_id=None,
        poke_interval=60,
        timeout=600
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
        task_id=dag_config.CLEAR_XCOM_CACHE_TASK_ID,
        python_callable=dag_task.clear_xcom_cache
    )

    close_connection_task = PythonOperator(
        task_id=dag_config.CLOSE_CONNECTION_TASK_ID,
        python_callable=dag_task.close_connection
    )

    """Setting up a tasks sequence
    """
    wait_for_add_products_sensor >> get_price_urls_from_table_urls_task
    get_price_urls_from_table_urls_task >> find_update_for_prices_task
    find_update_for_prices_task >> upload_updated_data_to_table_task
    upload_updated_data_to_table_task >> clear_xcom_cache_task
    clear_xcom_cache_task >> close_connection_task
