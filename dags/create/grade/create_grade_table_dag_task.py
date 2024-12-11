"""
File that contain functional of DAG-tasks.
"""
import pandas

from src import config
from src.database.postgres import postgres_db_constant
from dags.create.grade import create_grade_table_dag_config as dag_config
from dags.global_dag_config import client


def drop_grade_table_if_exists():
    """Drops the existing table 'grade' if it exists.
    """
    client.execute_sql(query=dag_config.DROP_GRADE_TABLE_QUERY, is_return=False)


def get_non_filtered_grades_from_table_feedbacks(**context):
    """Getting grades from table 'feedbacks' and push it
    to Xcom cash for next task.
    """
    non_filtered_grade_df: pandas.DataFrame = client.create_dataframe_by_sql(
        query=dag_config.SELECT_NON_FILTERED_GRADES_FROM_TABLE_FEEDBACK_QUERY
    )
    context['ti'].xcom_push(key='non_filtered_grade_df', value=non_filtered_grade_df)
    print(non_filtered_grade_df.columns)


def get_filtered_grades_from_table_feedbacks(**context):
    """Get second version of dataframe with filtered grades and push it
    to Xcom cash for next task.
    """
    filtered_grade_df: pandas.DataFrame = client.create_dataframe_by_sql(
        query=dag_config.SELECT_FILTERED_GRADES_FROM_TABLE_FEEDBACK_QUERY)
    context['ti'].xcom_push(key='filtered_grade_df', value=filtered_grade_df)


def calculate_means_for_non_filtered_grades(**context):
    """Function that calculate means values for dataframe with grades from past task
    and push result to Xcom cash in next task.
    """
    non_filtered_grade_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.GET_NON_FILTERED_GRADES_FROM_TABLE_FEEDBACKS_TASK_ID,
        key='non_filtered_grade_df'
    )

    non_filtered_grade_means_df: pandas.DataFrame = dag_config.create_dataframe_with_means_values(
        non_filtered_grade_df,
        is_filtered=False
    )
    context['ti'].xcom_push(key='non_filtered_grade_means_df', value=non_filtered_grade_means_df)


def calculate_means_for_filtered_grades(**context):
    """Function that calculate means values for dataframe with filtered grades from past task
    and push result to Xcom cash in next task.
    """
    filtered_grade_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.GET_FILTERED_GRADES_FROM_TABLE_FEEDBACKS_TASK_ID,
        key='filtered_grade_df'
    )

    filtered_grade_means_df: pandas.DataFrame = dag_config.create_dataframe_with_means_values(
        filtered_grade_df,
        is_filtered=True
    )
    context['ti'].xcom_push(key='filtered_grade_means_df', value=filtered_grade_means_df)


def create_final_dataframe(**context):
    """Function that merge 2 dataframes with means values in one final dataframe.
    """
    non_filtered_grade_means_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.CALCULATE_MEANS_FOR_NON_FILTERED_GRADES_TASK_ID,
        key='non_filtered_grade_means_df'
    )

    filtered_grade_means_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.CALCULATE_MEANS_FOR_FILTERED_GRADES_TASK_ID,
        key='filtered_grade_means_df'
    )

    final_df: pandas.DataFrame = non_filtered_grade_means_df.merge(
        filtered_grade_means_df,
        on=postgres_db_constant.PRODUCT_ID
    )

    context['ti'].xcom_push(key='final_df', value=final_df)


def create_table_grade_in_db(**kwargs):
    """Function that take dataframe from task 'create_final_dataframe' and upload him to our database.
    """
    final_df: pandas.DataFrame = kwargs['ti'].xcom_pull(
        task_ids=dag_config.CREATE_FINAL_DATAFRAME_TASK_ID,
        key='final_df'
    )

    final_df[postgres_db_constant.DATE] = dag_config.CURRENT_DATE
    final_df = final_df[[postgres_db_constant.PRODUCT_ID,
                         postgres_db_constant.DATE,
                         postgres_db_constant.MEAN_GRADE,
                         postgres_db_constant.MEAN_GRADE_FILTERED,
                         postgres_db_constant.MEDIAN_GRADE,
                         postgres_db_constant.MEDIAN_GRADE_FILTERED,
                         postgres_db_constant.MODE_GRADE,
                         postgres_db_constant.MODE_GRADE_FILTERED
                         ]]
    client.create_table_in_db_by_df(
        df=final_df,
        table_name=config.GRADE_TABLE,
        data_type=postgres_db_constant.grade_table_type_dict
    )

    # Add FK on table
    client.execute_sql(query=dag_config.ALTER_FOREIGN_KEY_IN_TABLE_GRADE_QUERY, is_return=False)
