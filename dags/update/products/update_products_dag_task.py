import pandas

from src import config
from src.database.postgres import postgres_db_constant

from dags.global_dag_config import client, parser
from dags.update.products import update_products_dag_config as dag_config


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

    product_df.drop_duplicates(inplace=True)

    context['ti'].xcom_push(key="product_df",
                            value=product_df)


def upload_updated_data_to_table(**context):
    """Function that pull dataframe with new data
    and upload them to table 'price_history' in our database.
    """
    product_df: pandas.DataFrame = context['ti'].xcom_pull(key="product_df",
                                                           task_ids=dag_config.FIND_UPDATE_FOR_PRODUCTS_TASK_ID)

    client.update_table_in_db_by_df(df=product_df,
                                    table_name=config.PRODUCT_TABLE,
                                    tmp_table_name=dag_config.TMP_PRODUCTS_TABLE_NAME,
                                    is_main_table=True,
                                    data_type=postgres_db_constant.products_table_type_dict,
                                    )
