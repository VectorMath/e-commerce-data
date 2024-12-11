from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config, global_dag_task
from dags.update.products import update_products_dag_config as dag_config
from dags.update.products import update_products_dag_task as dag_task

with DAG(
        dag_id=global_dag_config.UPDATE_PRODUCTS_TABLE_DAG_ID,
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
        task_id=global_dag_config.CLEAR_XCOM_CACHE_TASK_ID,
        python_callable=global_dag_task.clear_xcom_cache,
        op_kwargs={
            global_dag_config.XCOM_DAG_ID_COLUMN: global_dag_config.UPDATE_PRODUCTS_TABLE_DAG_ID
        }
    )

    """Setting up a tasks sequence
    """
    wait_for_add_products_sensor >> get_card_urls_from_table_products_task
    get_card_urls_from_table_products_task >> find_update_for_products_task
    find_update_for_products_task >> upload_updated_data_to_table_task
    upload_updated_data_to_table_task >> clear_xcom_cache_task
