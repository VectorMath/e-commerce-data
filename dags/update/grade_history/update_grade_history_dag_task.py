from dags.global_dag_config import client
from dags.update.grade_history import update_grade_history_dag_config as dag_config


def check_existing_of_grade_history_table():
    if client.execute_sql(query=dag_config.CHECK_EXISTING_QUERY, is_return=True)[0][0]:
        return dag_config.UPDATE_TABLE_GRADE_HISTORY_TASK_ID
    else:
        return dag_config.CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_TASK_ID


def create_table_grade_history_if_not_exists():
    client.execute_sql(
        query=dag_config.CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_QUERY,
        is_return=False
    )


def update_table_grade_history():
    client.execute_sql(
        query=dag_config.UPDATE_TABLE_GRADE_HISTORY_QUERY,
        is_return=False
    )
