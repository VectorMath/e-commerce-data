"""
DAG for creating a table with the actual grades for products.
Once completed, the table `grade` will be populated with the most recent grades.

The DAG have the following pipeline:
- Create table 'grade_history' if they don't exist.
- Upload data from table 'grade' into table 'grade_history'.
- Close connection.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.update.grade_history import update_grade_history_dag_config as dag_config
from dags.update.grade_history import update_grade_history_dag_task as dag_task

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
    create_table_grade_history_if_not_exists_task = PythonOperator(
        task_id=dag_config.CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_TASK_ID,
        python_callable=dag_task.create_table_grade_history_if_not_exists
    )

    update_table_grade_history_task = PythonOperator(
        task_id=dag_config.UPDATE_TABLE_GRADE_HISTORY_TASK_ID,
        python_callable=dag_task.update_table_grade_history
    )

    close_connection_task = PythonOperator(
        task_id=dag_config.CLOSE_CONNECTION_TASK_ID,
        python_callable=dag_task.close_connection
    )

    create_table_grade_history_if_not_exists_task >> update_table_grade_history_task >> close_connection_task