"""
DAG for removing from database the products, that already doesn't exist.

What's means 'doesn't exist'?
That means a products with bad status code on request by his urls.

The DAG have the following pipeline:
- In loop we make request in all urls for checking status code.
  After that push to XCOM list with 'bad' ids;
- Remove products from database;
- Clear XCOM cache and close connection;
"""
from airflow import DAG
from airflow.operators.python import PythonOperator

from dags import global_dag_config, global_dag_task
from dags.remove.products import remove_products_dag_config as dag_config
from dags.remove.products import remove_products_dag_task as dag_task

# Define the DAG
with DAG(
        dag_id=global_dag_config.REMOVE_PRODUCTS_FROM_DATABASE_DAG_ID,
        schedule_interval=global_dag_config.DAILY_REMOVE_DAG_PARAMETERS["schedule_interval"],
        max_active_runs=global_dag_config.DAILY_REMOVE_DAG_PARAMETERS["max_active_runs"],
        tags=global_dag_config.DAILY_REMOVE_DAG_PARAMETERS["tags"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
    """Define tasks on DAG
    """
    find_products_with_bad_status_code_task = PythonOperator(
        task_id=dag_config.FIND_PRODUCTS_WITH_BAD_RESPONSE_CODE_TASK_ID,
        python_callable=dag_task.find_products_with_bad_status_code,
        provide_context=True
    )

    remove_products_from_database_task = PythonOperator(
        task_id=dag_config.REMOVE_PRODUCTS_FROM_DATABASE_TASK_ID,
        python_callable=dag_task.remove_products_from_database,
        provide_context=True
    )

    clear_xcom_cache_task = PythonOperator(
        task_id=global_dag_config.CLEAR_XCOM_CACHE_TASK_ID,
        python_callable=global_dag_task.clear_xcom_cache,
        op_kwargs={
            global_dag_config.XCOM_DAG_ID_COLUMN: global_dag_config.REMOVE_PRODUCTS_FROM_DATABASE_DAG_ID
        }
    )

    """Setting up a tasks sequence
    """
    find_products_with_bad_status_code_task >> remove_products_from_database_task
    remove_products_from_database_task >> clear_xcom_cache_task