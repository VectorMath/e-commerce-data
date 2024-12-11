"""
DAG for creating a table with the actual price for products.
Once completed, the table `price` will be populated with the most recent prices.

The DAG have the following pipeline:
- Drop table 'price' from our database;
- From table 'price_history' we select last price for every product by window function
- Close connection to our database;
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config

from dags.create.price import create_price_table_dag_config as dag_config
from dags.create.price import create_price_table_dag_task as dag_task

# Define the DAG
with DAG(
        dag_id=global_dag_config.CREATE_PRICE_TABLE_DAG_ID,
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["create"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
    """Define sensor.
    """
    wait_for_update_price_history_sensor = ExternalTaskSensor(
        task_id=dag_config.WAIT_FOR_UPDATE_PRICE_HISTORY_SENSOR_ID,
        external_dag_id=global_dag_config.UPDATE_PRICE_HISTORY_TABLE_DAG_ID,
        external_task_id=global_dag_config.DEFAULT_SENSORS_PARAMETERS["external_task_id"],
        poke_interval=global_dag_config.DEFAULT_SENSORS_PARAMETERS["poke_interval"],
        timeout=global_dag_config.DEFAULT_SENSORS_PARAMETERS["timeout"]
    )

    """Define tasks on DAG
    """
    drop_price_table_task = PythonOperator(
        task_id=dag_config.DROP_TABLE_PRICE_TASK_ID,
        python_callable=dag_task.drop_price_table_if_exists
    )

    create_price_table_task = PythonOperator(
        task_id=dag_config.CREATE_TABLE_PRICE_TASK_ID,
        python_callable=dag_task.create_price_table_from_history
    )

    """Setting up a tasks sequence
    """
    wait_for_update_price_history_sensor >> drop_price_table_task >> create_price_table_task
