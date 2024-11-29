"""File with global constant values for DAGs.
"""
from dags.create_dags.price import create_price_table_dag_config as price_config
from dags.create_dags.grade import create_grade_table_dag_config as grade_config
from dags.update.grade_history import update_grade_history_dag_config as grade_history_config

# DAGs IDs.
CREATE_PRICE_TABLE_DAG_ID = price_config.DAG_ID
CREATE_GRADE_TABLE_DAG_ID = grade_config.DAG_ID
UPDATE_GRADE_HISTORY_TABLE_DAG_ID = grade_history_config.DAG_ID