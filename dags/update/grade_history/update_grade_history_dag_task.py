from src.database.postgres.ClientPostgres import ClientPostgres
from src.database.postgres.ConnectorPostgres import ConnectorPostgres

from dags.update.grade_history import update_grade_history_dag_config as dag_config

client: ClientPostgres = ClientPostgres(ConnectorPostgres())

def create_table_grade_history_if_not_exists():
    client.execute_sql(query=dag_config.CREATE_TABLE_GRADE_HISTORY_IF_NOT_EXISTS_QUERY, is_return=False)

def update_table_grade_history():
    client.execute_sql(query=dag_config.UPDATE_TABLE_GRADE_HISTORY_QUERY, is_return=False)

def close_connection():
    client.close_connection()