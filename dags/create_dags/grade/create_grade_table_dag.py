"""
DAG for creating a table with the actual grades for products.
Once completed, the table `grade` will be populated with the most recent grades.

The DAG have the following pipeline:
- Collect grades two types from table 'feedbacks' (non-filtered/filtered* grades)
and form it into dataframes;
- Create dataframe with different means values (mean, median and mode)
for every type of grades. In our case we have 2 types: non-filtered/filtered;
- Make final presentation of grades by merging our dataframes with means values;
- Create table 'grade' using final presentation in past step;
- Close connection and clear cache of Xcom;

*Filtered grade - the grade that have a not empty value in column 'comment'
and count of words in this comment must exceed a limit.
For value of limit response variable REQUIRED_COUNT_WORDS_FOR_FILTER in file create_grade_table_dag_config.py
"""
from airflow import DAG
from airflow.operators.python import PythonOperator

from dags.create_dags.grade import create_grade_table_dag_config as dag_config
from dags.create_dags.grade import create_grade_table_dag_task as dag_task

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
    drop_grade_table_task = PythonOperator(
        task_id=dag_config.DROP_TABLE_GRADE_TASK_ID,
        python_callable=dag_task.drop_grade_table_if_exists
    )

    get_non_filtered_grades_from_table_feedbacks_task = PythonOperator(
        task_id=dag_config.GET_NON_FILTERED_GRADES_FROM_TABLE_FEEDBACKS_TASK_ID,
        python_callable=dag_task.get_non_filtered_grades_from_table_feedbacks,
        provide_context=True
    )

    get_filtered_grades_from_table_feedback_task = PythonOperator(
        task_id=dag_config.GET_FILTERED_GRADES_FROM_TABLE_FEEDBACKS_TASK_ID,
        python_callable=dag_task.get_filtered_grades_from_table_feedbacks
    )

    calculate_means_for_non_filtered_grades_task = PythonOperator(
        task_id=dag_config.CALCULATE_MEANS_FOR_NON_FILTERED_GRADES_TASK_ID,
        python_callable=dag_task.calculate_means_for_non_filtered_grades,
        provide_context=True
    )

    calculate_means_for_filtered_grades_task = PythonOperator(
        task_id=dag_config.CALCULATE_MEANS_FOR_FILTERED_GRADES_TASK_ID,
        python_callable=dag_task.calculate_means_for_filtered_grades,
        provide_context=True
    )

    create_final_dataframe_task = PythonOperator(
        task_id=dag_config.CREATE_FINAL_DATAFRAME_TASK_ID,
        python_callable=dag_task.create_final_dataframe,
        provide_context=True
    )

    create_table_grade_in_db_task = PythonOperator(
        task_id=dag_config.CREATE_TABLE_GRADE_IN_DATABASE_TASK_ID,
        python_callable=dag_task.create_table_grade_in_db,
        provide_context=True
    )

    close_connection_task = PythonOperator(
        task_id=dag_config.CLOSE_CONNECTION_TASK_ID,
        python_callable=dag_task.close_postgres_connection
    )

    clear_xcom_cache_task = PythonOperator(task_id=dag_config.CLEAR_XCOM_CACHE_TASK_ID,
                                           python_callable=dag_task.clear_xcom_cache)

    """Setting up a tasks sequence
    """
    drop_grade_table_task >> [
        get_non_filtered_grades_from_table_feedbacks_task,
        get_filtered_grades_from_table_feedback_task
    ]

    get_non_filtered_grades_from_table_feedbacks_task >> calculate_means_for_non_filtered_grades_task

    get_filtered_grades_from_table_feedback_task >> calculate_means_for_filtered_grades_task

    [
        calculate_means_for_non_filtered_grades_task,
        calculate_means_for_filtered_grades_task
    ] >> create_final_dataframe_task

    create_final_dataframe_task >> create_table_grade_in_db_task

    create_table_grade_in_db_task >> clear_xcom_cache_task >> close_connection_task
