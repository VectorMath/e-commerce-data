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

from dags.create_dags.price import create_price_table_dag_config as dag_config
from dags.create_dags.price import create_price_table_dag_task as dag_task

# Define the DAG
with DAG(
        dag_id=dag_config.DAG_ID,
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["create"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
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

    close_connection_task = PythonOperator(
        task_id=dag_config.CLOSE_CONNECTION_TASK_ID,
        python_callable=dag_task.close_postgres_connection
    )

    """Setting up a tasks sequence
    """
    drop_price_table_task >> create_price_table_task >> close_connection_task
