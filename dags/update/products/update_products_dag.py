from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config
from dags.update.products import update_products_dag_config as dag_config
from dags.update.products import update_products_dag_task as dag_task

with DAG(
        dag_id=dag_config.DAG_ID,
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["update"],
        default_args=dag_config.DEFAULT_ARGS
):
    """Define sensor
    """
    wait_for_add_products_sensor = ExternalTaskSensor(
        task_id=dag_config.WAIT_FOR_ADD_PRODUCTS_SENSOR_ID,
        external_dag_id=global_dag_config.ADD_PRODUCT_IN_TABLE_DAG_ID,
        external_task_id=None,
        poke_interval=60,
        timeout=600
    )

    """Define tasks
    """
    get_card_urls_from_table_products_task = PythonOperator(
        task_id=dag_config.GET_CARD_URLS_FROM_TABLE_URLS_TASK_ID,
        python_callable=dag_task.get_card_urls_from_table_urls,
        provide_context=True
    )

    find_update_for_products_task = PythonOperator(
        task_id=dag_config.FIND_UPDATE_FOR_PRODUCTS_TASK_ID,
        python_callable=dag_task.find_update_for_products,
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
    wait_for_add_products_sensor >> get_card_urls_from_table_products_task
    get_card_urls_from_table_products_task >> find_update_for_products_task
    find_update_for_products_task >> upload_updated_data_to_table_task
    upload_updated_data_to_table_task >> clear_xcom_cache_task
    clear_xcom_cache_task >> close_connection_task
