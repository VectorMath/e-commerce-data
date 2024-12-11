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
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config
from dags.update.grade_history import update_grade_history_dag_config as dag_config
from dags.update.grade_history import update_grade_history_dag_task as dag_task

# Define the DAG
with (DAG(
        dag_id=global_dag_config.UPDATE_GRADE_HISTORY_TABLE_DAG_ID,
        schedule_interval=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["schedule_interval"],
        max_active_runs=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["max_active_runs"],
        tags=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["tags"],
        default_args=dag_config.DEFAULT_ARGS
) as dag):
    """Define sensor, that wait complete
    """
    wait_for_create_table_grade_dag_sensor = ExternalTaskSensor(
        task_id=dag_config.WAIT_FOR_CREATE_TABLE_GRADE_TASK_ID,
        external_dag_id=global_dag_config.CREATE_GRADE_TABLE_DAG_ID,
        external_task_id=global_dag_config.DEFAULT_SENSORS_PARAMETERS["external_task_id"],
        poke_interval=global_dag_config.DEFAULT_SENSORS_PARAMETERS["poke_interval"],
        timeout=global_dag_config.DEFAULT_SENSORS_PARAMETERS["timeout"]
    )

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

    wait_for_create_table_grade_dag_sensor >> create_table_grade_history_if_not_exists_task
    create_table_grade_history_if_not_exists_task >> update_table_grade_history_task
