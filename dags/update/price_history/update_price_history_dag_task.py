import pandas

from src import config
from src.database.postgres import postgres_db_constant

from dags.global_dag_config import client, parser
from dags.update.price_history import update_price_history_dag_config as dag_config


def get_price_urls_from_table_urls(**context):
    """Function that get urls list of price history
    and push them to XCOM.
    """
    price_urls: list[str] = list(client.create_dataframe_by_sql(
        query=dag_config.SELECT_PRICE_URLS_FROM_TABLE_PRICE_HISTORY_QUERY
    ).iloc[:, 0])

    context['ti'].xcom_push(key="price_urls", value=price_urls)


def find_update_for_prices(**context):
    """Function that pull urls of price history from XCOM
    and parse actual history of prices. After that push dataframe with new_data in XCOM.
    """
    price_urls: list[str] = context['ti'].xcom_pull(
        key="price_urls",
        task_ids=dag_config.GET_PRICE_URLS_FROM_TABLE_URLS_TASK_ID
    )

    price_history_df: pandas.DataFrame = pandas.DataFrame()

    for price_url in price_urls:
        price_history_df = pandas.concat([price_history_df,
                                          parser.parse_product_price_history(price_url=price_url)])

    context['ti'].xcom_push(key="price_history_df",
                            value=price_history_df)


def upload_updated_data_to_table(**context):
    """Function that pull dataframe with new data
    and upload them to table 'price_history' in our database.
    """
    price_history_df: pandas.DataFrame = context['ti'].xcom_pull(
        key="price_history_df",
        task_ids=dag_config.FIND_UPDATE_FOR_PRICES_TASK_ID
    )

    client.update_table_in_db_by_df(df=price_history_df,
                                    table_name=config.PRICE_HISTORY_TABLE,
                                    tmp_table_name=dag_config.TMP_PRICE_HISTORY_TABLE_NAME,
                                    is_main_table=False,
                                    data_type=postgres_db_constant.price_history_type_dict,
                                    )
