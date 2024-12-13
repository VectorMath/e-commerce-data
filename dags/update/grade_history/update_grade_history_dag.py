"""
DAG for creating a table with the actual grades for products.
Once completed, the table `grade` will be populated with the most recent grades.

The DAG have the following pipeline:
- Create table 'grade_history' if they don't exist.
- Upload data from table 'grade' into table 'grade_history'.
- Close connection.
"""

from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.sensors.external_task import ExternalTaskSensor

from dags import global_dag_config, global_dag_task
from dags.update.grade_history import update_grade_history_dag_config as dag_config
from dags.update.grade_history import update_grade_history_dag_task as dag_task
from src import config
from src.database.postgres import postgres_db_constant

# Define the DAG
with DAG(
        dag_id=global_dag_config.UPDATE_GRADE_HISTORY_TABLE_DAG_ID,
        schedule_interval=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["schedule_interval"],
        max_active_runs=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["max_active_runs"],
        tags=global_dag_config.DAILY_UPDATE_DAG_PARAMETERS["tags"],
        default_args=dag_config.DEFAULT_ARGS
) as dag:
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
    check_existing_of_table_task = BranchPythonOperator(
        task_id="check_existing_of_table",
        python_callable=dag_task.check_existing_of_grade_history_table,
        provide_context=True
    )

    create_table_grade_history_if_not_exists_task = PythonOperator(
        task_id=dag_config.CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_TASK_ID,
        python_callable=dag_task.create_table_grade_history_if_not_exists
    )

    update_table_grade_history_task = PythonOperator(
        task_id=dag_config.UPDATE_TABLE_GRADE_HISTORY_TASK_ID,
        python_callable=dag_task.update_table_grade_history
    )

    sort_data_in_grade_history_task = PythonOperator(
        task_id=dag_config.SORT_DATA_IN_GRADE_HISTORY_TASK_ID,
        python_callable=global_dag_task.sort_data_in_table,
        op_kwargs={
            "table_name": config.GRADE_HISTORY_TABLE,
            "index": postgres_db_constant.INDEX_GRADE_HISTORY
        }
    )

    update_table_grade_history_after_create_task = PythonOperator(
        task_id=dag_config.UPDATE_TABLE_GRADE_HISTORY_AFTER_CREATE_TASK_ID,
        python_callable=dag_task.update_table_grade_history
    )

    sort_data_in_grade_history_after_create_task = PythonOperator(
        task_id=dag_config.SORT_DATA_IN_GRADE_HISTORY_AFTER_CREATE_TASK_ID,
        python_callable=global_dag_task.sort_data_in_table,
        op_kwargs={
            "table_name": config.GRADE_HISTORY_TABLE,
            "index": postgres_db_constant.INDEX_GRADE_HISTORY
        }
    )

    """Define the dependencies"""
    wait_for_create_table_grade_dag_sensor >> check_existing_of_table_task
    check_existing_of_table_task >> [create_table_grade_history_if_not_exists_task, update_table_grade_history_task]
    create_table_grade_history_if_not_exists_task >> update_table_grade_history_after_create_task >> sort_data_in_grade_history_after_create_task
    update_table_grade_history_task >> sort_data_in_grade_history_task
