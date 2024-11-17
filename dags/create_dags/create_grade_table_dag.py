"""
DAG for creating a table with the actual grades for products.
Once completed, the table `grade` will be populated with the most recent grades.
"""
import pandas as pd
from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.operators.python import PythonOperator

from src import config
from src.database.postgres import postgres_db_constant
from src.database.postgres.ConnectorPostgres import ConnectorPostgres
from src.database.postgres.ClientPostgres import ClientPostgres

# Create an instance of the PostgreSQL client
client: ClientPostgres = ClientPostgres(ConnectorPostgres())

# Default arguments for the DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

# Count words in column 'comment' in table 'feedbacks'.
REQUIRED_COUNT_WORDS_FOR_FILTER: int = 10

# SQL queries
DROP_GRADE_TABLE_QUERY: str = f"""DROP TABLE IF EXISTS {config.GRADE_TABLE};"""

GET_GRADES_FROM_FEEDBACK_TABLE: str = f"""
SELECT {postgres_db_constant.PRODUCT_ID},
       {postgres_db_constant.GRADE}
FROM {config.FEEDBACKS_TABLE}
;
"""

GET_FILTERED_GRADES_FROM_FEEDBACK_TABLE: str = f"""
SELECT {postgres_db_constant.PRODUCT_ID},
       {postgres_db_constant.GRADE}
FROM {config.FEEDBACKS_TABLE}
WHERE (
    {postgres_db_constant.COMMENT} IS NOT NULL
    AND {postgres_db_constant.COMMENT} <> ''
    )
    AND array_length(regexp_split_to_array({postgres_db_constant.COMMENT}, '\s+'), 1) > {REQUIRED_COUNT_WORDS_FOR_FILTER}
;
"""


# Python functions that will be used in callbacks
def create_dataframe_with_means_values(df: pd.DataFrame, is_filtered: bool) -> pd.DataFrame:
    mean_grade_col: str = postgres_db_constant.MEAN_GRADE
    median_grade_col: str = postgres_db_constant.MEDIAN_GRADE
    mode_grade_col: str = postgres_db_constant.MODE_GRADE

    if is_filtered:
        mean_grade_col = postgres_db_constant.MEAN_GRADE_FILTERED
        median_grade_col = postgres_db_constant.MEDIAN_GRADE_FILTERED
        mode_grade_col = postgres_db_constant.MODE_GRADE_FILTERED

    mean_df: pd.DataFrame = df.groupby(postgres_db_constant.PRODUCT_ID).mean().rename(
        columns={postgres_db_constant.GRADE: mean_grade_col})
    median_df: pd.DataFrame = df.groupby(postgres_db_constant.PRODUCT_ID).median().rename(
        columns={postgres_db_constant.GRADE: median_grade_col})
    mode_df: pd.DataFrame = df.groupby(postgres_db_constant.PRODUCT_ID).agg(lambda x: x.mode()[0]).rename(
        columns={postgres_db_constant.GRADE: mode_grade_col})

    return mean_df.merge(median_df,
                         on=postgres_db_constant.PRODUCT_ID).merge(mode_df,
                                                                   on=postgres_db_constant.PRODUCT_ID).reset_index()


# Python callback functions to execute SQL queries
def drop_grade_table_if_exists():
    """Drops the existing grade table if it exists.
    """
    client.execute_sql(query=DROP_GRADE_TABLE_QUERY, is_return=False)


def get_grades_from_feedback_table(**kwargs):
    """Getting grades from table 'feedbacks'.
    """
    grade_df = client.create_dataframe_by_sql(query=GET_GRADES_FROM_FEEDBACK_TABLE)
    kwargs['ti'].xcom_push(key='grade_df', value=grade_df)
    print(grade_df.columns)


def get_filtered_grades_from_feedback_table(**kwargs):
    """Get second version of dataframe with filtered grades
    """
    filtered_grade_df = client.create_dataframe_by_sql(query=GET_FILTERED_GRADES_FROM_FEEDBACK_TABLE)
    kwargs['ti'].xcom_push(key='filtered_grade_df', value=filtered_grade_df)
    print(filtered_grade_df.columns)


def calculate_means_for_grades(**kwargs):
    grade_df = kwargs['ti'].xcom_pull(task_ids='get_grades_from_feedback_table', key='grade_df')
    grade_means_df = create_dataframe_with_means_values(grade_df, is_filtered=False)
    kwargs['ti'].xcom_push(key='grade_means_df', value=grade_means_df)
    print(grade_means_df.columns)


def calculate_means_for_filtered_grades(**kwargs):
    filtered_grade_df = kwargs['ti'].xcom_pull(task_ids='get_filtered_grades_from_feedback_table',
                                               key='filtered_grade_df')
    filtered_grade_means_df = create_dataframe_with_means_values(filtered_grade_df, is_filtered=True)
    kwargs['ti'].xcom_push(key='filtered_grade_means_df', value=filtered_grade_means_df)
    print(filtered_grade_means_df.columns)


def create_final_dataframe(**kwargs):
    grade_means_df = kwargs['ti'].xcom_pull(task_ids='calculate_means_for_grades', key='grade_means_df')
    filtered_grade_means_df = kwargs['ti'].xcom_pull(task_ids='calculate_means_for_filtered_grades',
                                                     key='filtered_grade_means_df')
    result_df = grade_means_df.merge(filtered_grade_means_df, on=postgres_db_constant.PRODUCT_ID)
    kwargs['ti'].xcom_push(key='result_df', value=result_df)


def create_table_grade_in_db(**kwargs):
    result_df = kwargs['ti'].xcom_pull(task_ids='create_final_dataframe', key='result_df')
    result_df = result_df[[postgres_db_constant.PRODUCT_ID,
                           postgres_db_constant.MEAN_GRADE,
                           postgres_db_constant.MEAN_GRADE_FILTERED,
                           postgres_db_constant.MEDIAN_GRADE,
                           postgres_db_constant.MEDIAN_GRADE_FILTERED,
                           postgres_db_constant.MODE_GRADE,
                           postgres_db_constant.MODE_GRADE_FILTERED,]]
    client.create_table_in_db_by_df(df=result_df,
                                    table_name=config.GRADE_TABLE,
                                    data_type=postgres_db_constant.grade_table_type_dict)


def close_postgres_connection():
    """Closes the PostgreSQL connection.
    """
    client.close_connection()


# Define the DAG
with DAG(
        dag_id="create-grade-table",
        schedule_interval="@daily",
        max_active_runs=1,
        tags=["create"],
        default_args=DEFAULT_ARGS
) as dag:
    # Task 1: Drop the existing price table
    drop_grade_table_task = PythonOperator(
        task_id="drop_grade_table",
        python_callable=drop_grade_table_if_exists
    )

    get_grades_from_feedback_table_task = PythonOperator(task_id="get_grades_from_feedback_table",
                                                         python_callable=get_grades_from_feedback_table,
                                                         provide_context=True)

    get_filtered_grades_from_feedback_table_task = PythonOperator(task_id="get_filtered_grades_from_feedback_table",
                                                                  python_callable=get_filtered_grades_from_feedback_table)

    calculate_means_for_grades_task = PythonOperator(task_id="calculate_means_for_grades",
                                                     python_callable=calculate_means_for_grades,
                                                     provide_context=True)

    calculate_means_for_filtered_grades_task = PythonOperator(task_id="calculate_means_for_filtered_grades",
                                                              python_callable=calculate_means_for_filtered_grades,
                                                              provide_context=True)

    create_final_dataframe_task = PythonOperator(task_id="create_final_dataframe",
                                                 python_callable=create_final_dataframe,
                                                 provide_context=True)

    create_table_grade_in_db_task = PythonOperator(task_id="create_table_grade_in_db",
                                                   python_callable=create_table_grade_in_db,
                                                   provide_context=True)

    close_connection_task = PythonOperator(task_id="close_connection",
                                           python_callable=close_postgres_connection)

    drop_grade_table_task >> [get_grades_from_feedback_table_task, get_filtered_grades_from_feedback_table_task]

    get_grades_from_feedback_table_task >> calculate_means_for_grades_task

    get_filtered_grades_from_feedback_table_task >> calculate_means_for_filtered_grades_task

    [calculate_means_for_grades_task, calculate_means_for_filtered_grades_task] >> create_final_dataframe_task

    create_final_dataframe_task >> create_table_grade_in_db_task

    create_table_grade_in_db_task >> close_connection_task
