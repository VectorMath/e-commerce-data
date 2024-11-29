"""
Here contains constants values and common functions
for DAG-files 'update_grade_history_dag.py' and 'update_grade_history_dag_task.py'
"""
from airflow.utils.dates import days_ago

from src import config
from src.database.postgres import postgres_db_constant

"""IDs for DAG and tasks."""
DAG_ID = "update-grade-history"
CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_TASK_ID = "create_table_grade_history_if_not_exists"
GET_ACTUAL_GRADES_FROM_TABLE_GRADE_TASK_ID = "get_actual_grades_from_table_grade"
UPDATE_TABLE_GRADE_HISTORY_TASK_ID = "update_table_grade_history"
CLOSE_CONNECTION_TASK_ID = "close_connection"

# Default arguments for DAG
DEFAULT_ARGS: dict = {
    'start_date': days_ago(1),
    'owner': 'eugene',
    'poke_interval': 600
}

# List of columns table 'grade'
COLUMN_LIST: list[str] = list(postgres_db_constant.grade_table_type_dict.keys())

# List with key and values of table 'grade'
KEY_VALUE_LIST = ', '.join(f"{key} {value}" for key, value in postgres_db_constant.grade_table_type_dict.items())

# SQL Queries
CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_QUERY: str = f"""
CREATE TABLE IF NOT EXISTS {config.GRADE_HISTORY_TABLE} ({KEY_VALUE_LIST});
ALTER TABLE {config.GRADE_HISTORY_TABLE}
ADD CONSTRAINT fk_product_id
FOREIGN KEY ({postgres_db_constant.PRODUCT_ID})
REFERENCES public.{config.PRODUCT_TABLE}({postgres_db_constant.PRODUCT_ID})
ON DELETE CASCADE;
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
