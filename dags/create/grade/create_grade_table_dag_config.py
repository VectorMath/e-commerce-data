"""
Here contains constants values and common functions
for DAG-files 'create_grade_table_dag.py' and 'create_grade_table_dag_task.py'
"""
from datetime import datetime

import pandas
from airflow.utils.dates import days_ago

from src.database.postgres import postgres_db_constant
from src import config

"""IDs for DAG and tasks."""
WAIT_FOR_UPDATE_FEEDBACKS_SENSOR_ID: str = "wait_for_update_feedbacks"
DROP_TABLE_GRADE_TASK_ID: str = "drop_table_grade"
GET_NON_FILTERED_GRADES_FROM_TABLE_FEEDBACKS_TASK_ID: str = "get_non_filtered_grades_from_table_feedbacks"
GET_FILTERED_GRADES_FROM_TABLE_FEEDBACKS_TASK_ID: str = "get_filtered_grades_from_table_feedbacks"
CALCULATE_MEANS_FOR_NON_FILTERED_GRADES_TASK_ID: str = "calculate_means_for_non_filtered_grades"
CALCULATE_MEANS_FOR_FILTERED_GRADES_TASK_ID: str = "calculate_means_for_filtered_grades"
CREATE_FINAL_DATAFRAME_TASK_ID: str = "create_final_dataframe"
CREATE_TABLE_GRADE_IN_DATABASE_TASK_ID: str = "create_table_grade_in_database"

# Default arguments for the DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

# Count words in column 'comment' in table 'feedbacks'.
REQUIRED_COUNT_WORDS_FOR_FILTER: int = 10

# Current date
CURRENT_DATE: str = datetime.now().strftime("%Y-%m-%d")

# SQL queries
DROP_GRADE_TABLE_QUERY: str = f"""DROP TABLE IF EXISTS {config.GRADE_TABLE};"""

SELECT_NON_FILTERED_GRADES_FROM_TABLE_FEEDBACK_QUERY: str = f"""
SELECT {postgres_db_constant.PRODUCT_ID},
       {postgres_db_constant.GRADE}
FROM {config.FEEDBACKS_TABLE}
;
"""

SELECT_FILTERED_GRADES_FROM_TABLE_FEEDBACK_QUERY: str = f"""
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

ALTER_FOREIGN_KEY_IN_TABLE_GRADE_QUERY: str = f"""
ALTER TABLE {config.GRADE_TABLE}
ADD CONSTRAINT fk_product_id
FOREIGN KEY ({postgres_db_constant.PRODUCT_ID})
REFERENCES public.{config.PRODUCT_TABLE}({postgres_db_constant.PRODUCT_ID})
ON DELETE CASCADE;
"""

# Python functions that will be used in callbacks
def create_dataframe_with_means_values(df: pandas.DataFrame, is_filtered: bool) -> pandas.DataFrame:
    """Method that take dataframe with grades and create
    new dataframe with means values for every product id.

    If your parameter df contain filtered grades, insert True in parameter 'is_filtered'
    and your columns names will get subfix 'filtered'.

    :param df: Dataframe with grades.
    :param is_filtered: bool-value that response for subfix of columns with mean values.

    :return: Dataframe with means values for every product id.
    """
    mean_grade_col: str = postgres_db_constant.MEAN_GRADE
    median_grade_col: str = postgres_db_constant.MEDIAN_GRADE
    mode_grade_col: str = postgres_db_constant.MODE_GRADE

    if is_filtered:
        mean_grade_col: str = postgres_db_constant.MEAN_GRADE_FILTERED
        median_grade_col: str = postgres_db_constant.MEDIAN_GRADE_FILTERED
        mode_grade_col: str = postgres_db_constant.MODE_GRADE_FILTERED

    mean_df: pandas.DataFrame = df.groupby(postgres_db_constant.PRODUCT_ID).mean().rename(
        columns={postgres_db_constant.GRADE: mean_grade_col})
    median_df: pandas.DataFrame = df.groupby(postgres_db_constant.PRODUCT_ID).median().rename(
        columns={postgres_db_constant.GRADE: median_grade_col})
    mode_df: pandas.DataFrame = df.groupby(postgres_db_constant.PRODUCT_ID).agg(lambda x: x.mode()[0]).rename(
        columns={postgres_db_constant.GRADE: mode_grade_col})

    return mean_df.merge(median_df,
                         on=postgres_db_constant.PRODUCT_ID).merge(mode_df,
                                                                   on=postgres_db_constant.PRODUCT_ID).reset_index()
