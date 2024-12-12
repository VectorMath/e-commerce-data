"""
File that contain functional of DAG-tasks who using in few DAGs.
"""

from dags import global_dag_config


def sort_data_in_table(table_name: str, index: str):
    """Function that will sort rows in table.
    :param table_name: name of table that rows need to be sorted.
    :param index: Name of index in SQL.
    """
    query: str = f"""
    CLUSTER {table_name} USING {index};
    """
    global_dag_config.client.execute_sql(query=query, is_return=False)


def clear_xcom_cache(dag_id: str):
    """Function that delete rows from table 'xcom' in schema 'airflow' in our database.
    :param dag_id: ID of DAG that XCOM cache need to be clear.
    """
    query: str = f"""
    DELETE FROM {global_dag_config.AIRFLOW_DB_SCHEMA}.{global_dag_config.XCOM_TABLE_NAME}
    WHERE {global_dag_config.XCOM_DAG_ID_COLUMN} = '{dag_id}';
    """
    global_dag_config.client.execute_sql(query=query, is_return=False)


def close_connection():
    """Closes the PostgreSQL connection.
    """
    global_dag_config.client.close_connection()
