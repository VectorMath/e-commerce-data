import pandas

from src import config
from src.parser.WB.ParserWB import ParserWB
from src.database.postgres.ClientPostgres import ClientPostgres
from src.database.postgres.ConnectorPostgres import ConnectorPostgres
from src.database.postgres import postgres_db_constant

from dags.update.products import update_products_dag_config as dag_config

parser = ParserWB()
client = ClientPostgres(ConnectorPostgres())


def get_card_urls_from_table_urls(**context):
    """Function that get urls list of products personal info
    and push them to XCOM.
    """
    product_urls: list[str] = list(client.create_dataframe_by_sql(
        query=dag_config.SELECT_CARD_URLS_FROM_TABLE_PRICE_HISTORY_QUERY
    ).iloc[:, 0])

    context['ti'].xcom_push(key="product_urls", value=product_urls)


def find_update_for_products(**context):
    """Function that pull urls of products from XCOM
    and parse info of products. After that push dataframe with new_data in XCOM.
    """
    product_urls: list[str] = context['ti'].xcom_pull(
        key="product_urls",
        task_ids=dag_config.GET_CARD_URLS_FROM_TABLE_URLS_TASK_ID
    )

    product_df: pandas.DataFrame = pandas.DataFrame()

    for product_url in product_urls:
        product_df = pandas.concat([product_df,
                                    parser.parse_product(product_url)])

    context['ti'].xcom_push(key="product_df",
                            value=product_df)


def upload_updated_data_to_table(**context):
    """Function that pull dataframe with new data
    and upload them to table 'price_history' in our database.
    """
    product_df = context['ti'].xcom_pull(key="product_df",
                                         task_ids=dag_config.FIND_UPDATE_FOR_PRODUCTS_TASK_ID)
    client.update_table_in_db_by_df(df=product_df,
                                    table_name=config.PRODUCT_TABLE,
                                    tmp_table_name=dag_config.TMP_PRODUCTS_TABLE_NAME,
                                    is_main_table=False,
                                    data_type=postgres_db_constant.products_table_type_dict,
                                    )


def clear_xcom_cache():
    """Function that delete rows from table 'xcom' in schema 'airflow' in our database.
    """
    client.execute_sql(dag_config.DELETE_XCOM_CACHE_QUERY, is_return=False)


def close_connection():
    """Closes the PostgreSQL connection.
    """
    client.close_connection()
