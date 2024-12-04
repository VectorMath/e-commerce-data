"""
File that contain functional of DAG-tasks.
"""
import requests
import logging

from dags.remove.products import remove_products_dag_config as dag_config
from src import config

from src.database.postgres.ClientPostgres import ClientPostgres
from src.database.postgres.ConnectorPostgres import ConnectorPostgres

from src.database.postgres import postgres_db_constant

client = ClientPostgres(ConnectorPostgres())


def find_products_with_bad_status_code(**context):
    """Function that check status code of product url.
    If url have bad status code (in our case that >=400)
    We append this url to list.

    In the end we push list with invalid urls in XCOM cache.
    """
    df_urls = client.create_dataframe_by_sql(query=dag_config.SELECT_ALL_DATA_FROM_TABLE_URLS_QUERY)
    ids_with_bad_status_code: list[int] = []

    for product_id, url in zip(df_urls[postgres_db_constant.PRODUCT_ID],
                               df_urls[postgres_db_constant.PRODUCT_CARD_JSON]):
        if requests.get(url).status_code >= 400:
            ids_with_bad_status_code.append(product_id)

    if len(ids_with_bad_status_code) == df_urls.shape[0]:
        raise Exception("Something go wrong. All urls are invalid")
    else:
        context['ti'].xcom_push(key='ids_with_bad_status_code',
                                value=ids_with_bad_status_code)
        logging.info(msg=f"Table {config.URLS_TABLE} have {len(ids_with_bad_status_code)} invalid products")


def remove_products_from_database(**context):
    """Function that remove product with bad status code from database.
    We take list of product_id from previous task and insert them into our SQL query.
    In case when we don't have ids, function just go to the next task.
    """
    ids_with_bad_status_code = context['ti'].xcom_pull(
        task_ids=dag_config.FIND_PRODUCTS_WITH_BAD_RESPONSE_CODE_TASK_ID,
        key='ids_with_bad_status_code')

    if len(ids_with_bad_status_code) > 0:
        delete_query = f"""
        DELETE FROM {config.PRODUCT_TABLE}
        WHERE {postgres_db_constant.PRODUCT_ID} IN ({ids_with_bad_status_code})
        """
        client.execute_sql(query=delete_query, is_return=False)
    else:
        logging.info(msg="Nothing to remove. Go to next task.")


def clear_xcom_cache():
    """Function that delete rows from table 'xcom' in schema 'airflow' in our database.
    """
    client.execute_sql(dag_config.DELETE_XCOM_CACHE_QUERY, is_return=False)


def close_connection():
    """Closes the PostgreSQL connection.
    """
    client.close_connection()
