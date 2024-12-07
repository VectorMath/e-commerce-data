"""
DAG for adding new products in our database.

The DAG have the following pipeline:
- Parse ID of products;
- Create urls for products;
- Parse products personal info;
- Parse price history of products;
- Parse feedbacks of products;
- Upload new data in our database;
- Clear XCOM cache;
- Close connection;
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config
from dags.add.products import add_products_dag_config as dag_config
from dags.add.products import add_products_dag_task as dag_task

# Define the DAG
with DAG(
        dag_id=dag_config.DAG_ID,
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["add"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
    """Define sensor, that wait complete
    """
    wait_for_removing_products_sensor = ExternalTaskSensor(
        task_id=dag_config.WAIT_FOR_REMOVING_PRODUCTS_SENSOR_ID,
        external_dag_id=global_dag_config.REMOVE_PRODUCTS_FROM_DATABASE_DAG_ID,
        external_task_id=None,
        poke_interval=60,
        timeout=600
    )

    """Define tasks on DAG
    """
    parse_id_from_product_list_task = PythonOperator(
        task_id=dag_config.PARSE_ID_FROM_PRODUCT_LIST_TASK_ID,
        python_callable=dag_task.parse_id_from_product_list,
        provide_context=True
    )

    parse_urls_of_products_task = PythonOperator(
        task_id=dag_config.PARSE_URLS_OF_PRODUCTS_TASK_ID,
        python_callable=dag_task.parse_urls_of_products,
        provide_context=True
    )

    parse_products_personal_info_task = PythonOperator(
        task_id=dag_config.PARSE_PRODUCTS_PERSONAL_INFO_TASK_ID,
        python_callable=dag_task.parse_products_personal_info,
        provide_context=True
    )

    parse_price_history_task = PythonOperator(
        task_id=dag_config.PARSE_PRICE_HISTORY_TASK_ID,
        python_callable=dag_task.parse_price_history,
        provide_context=True
    )

    parse_feedbacks_task = PythonOperator(
        task_id=dag_config.PARSE_FEEDBACKS_TASK_ID,
        python_callable=dag_task.parse_feedbacks,
        provide_context=True
    )

    upload_new_data_in_products_task = PythonOperator(
        task_id=dag_config.UPLOAD_NEW_DATA_IN_PRODUCTS_TASK_ID,
        python_callable=dag_task.upload_new_data_in_products,
        provide_context=True
    )

    upload_new_data_in_urls_task = PythonOperator(
        task_id=dag_config.UPLOAD_NEW_DATA_IN_URLS_TASK_ID,
        python_callable=dag_task.upload_new_data_in_urls,
        provide_context=True
    )

    upload_new_data_in_price_history_task = PythonOperator(
        task_id=dag_config.UPLOAD_NEW_DATA_IN_PRICE_HISTORY_TASK_ID,
        python_callable=dag_task.upload_new_data_in_price_history,
        provide_context=True
    )

    upload_new_data_in_feedbacks_task = PythonOperator(
        task_id=dag_config.UPLOAD_NEW_DATA_IN_FEEDBACKS_TASK_ID,
        python_callable=dag_task.upload_new_data_in_feedbacks,
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
    wait_for_removing_products_sensor >> parse_id_from_product_list_task
    parse_id_from_product_list_task >> parse_urls_of_products_task
    parse_urls_of_products_task >> [parse_products_personal_info_task,
                                    parse_price_history_task,
                                    parse_feedbacks_task]

    [parse_products_personal_info_task,
     parse_price_history_task,
     parse_feedbacks_task] >> upload_new_data_in_products_task

    upload_new_data_in_products_task >> [upload_new_data_in_urls_task,
                                         upload_new_data_in_price_history_task,
                                         upload_new_data_in_feedbacks_task]

    [upload_new_data_in_urls_task,
     upload_new_data_in_price_history_task,
     upload_new_data_in_feedbacks_task] >> clear_xcom_cache_task >> close_connection_task
