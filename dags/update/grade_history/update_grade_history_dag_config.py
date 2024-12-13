"""
Here contains constants values and common functions
for DAG-files 'update_grade_history_dag.py' and 'update_grade_history_dag_task.py'
"""
from airflow.utils.dates import days_ago

from dags import global_dag_config
from src import config
from src.database.postgres import postgres_db_constant

"""IDs for DAG and tasks."""
WAIT_FOR_CREATE_TABLE_GRADE_TASK_ID: str = "wait_for_create_table_grade"
CHECK_EXISTING_OF_GRADE_HISTORY_TABLE_TASK_ID: str = "check_existing_of_grade_history_table"
CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_TASK_ID: str = "create_table_grade_history_if_not_exists"
GET_ACTUAL_GRADES_FROM_TABLE_GRADE_TASK_ID: str = "get_actual_grades_from_table_grade"
UPDATE_TABLE_GRADE_HISTORY_TASK_ID: str = "update_table_grade_history"
SORT_DATA_IN_GRADE_HISTORY_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID + f"_{config.GRADE_HISTORY_TABLE}"
UPDATE_TABLE_GRADE_HISTORY_AFTER_CREATE_TASK_ID: str = "update_table_grade_history_after_create"
SORT_DATA_IN_GRADE_HISTORY_AFTER_CREATE_TASK_ID: str = global_dag_config.SORT_DATA_IN_TABLE_TASK_ID + f"_{config.GRADE_HISTORY_TABLE}_after_create"

# Default arguments for DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

# List of columns table 'grade'
COLUMN_LIST: list[str] = list(postgres_db_constant.grade_table_type_dict.keys())

# List with key and values of table 'grade'
KEY_VALUE_LIST: str = ', '.join(f"{key} {value}" for key, value in postgres_db_constant.grade_table_type_dict.items())

# SQL Queries
CHECK_EXISTING_QUERY: str = f"""
        SELECT EXISTS (
            SELECT 1 
            FROM information_schema.tables 
            WHERE table_name = '{config.GRADE_HISTORY_TABLE}'
        );
    """

CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_QUERY: str = f"""
CREATE TABLE IF NOT EXISTS {config.GRADE_HISTORY_TABLE} ({KEY_VALUE_LIST});
ALTER TABLE {config.GRADE_HISTORY_TABLE}
ADD CONSTRAINT fk_product_id
FOREIGN KEY ({postgres_db_constant.PRODUCT_ID})
REFERENCES public.{config.PRODUCT_TABLE}({postgres_db_constant.PRODUCT_ID})
ON DELETE CASCADE;

CREATE INDEX IF NOT EXISTS {postgres_db_constant.INDEX_GRADE_HISTORY} 
ON public.{config.GRADE_HISTORY_TABLE} ({postgres_db_constant.PRODUCT_ID}, {postgres_db_constant.DATE});
"""

UPDATE_TABLE_GRADE_HISTORY_QUERY: str = f"""
INSERT INTO {config.GRADE_HISTORY_TABLE} ({', '.join(COLUMN_LIST)})
SELECT {', '.join(COLUMN_LIST)}
FROM {config.GRADE_TABLE}
WHERE NOT EXISTS (
    SELECT 1
    FROM {config.GRADE_HISTORY_TABLE}
    WHERE {config.GRADE_HISTORY_TABLE}."{postgres_db_constant.DATE}" = {config.GRADE_TABLE}."{postgres_db_constant.DATE}"
);
"""
