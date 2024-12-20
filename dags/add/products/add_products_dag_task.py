"""
File that contain functional of DAG-tasks.
"""
import pandas

from dags.global_dag_config import client
from dags.global_dag_config import parser

from dags.add.products import add_products_dag_config as dag_config

from src import config

from src.parser.WB.AsyncRequesterWB import AsyncRequesterWB

from src.database.postgres import postgres_db_constant


def parse_id_from_product_list(**context):
    """Function that will parse id of products from products list.
    After that push that into XCOM.
    """
    product_list_df: pandas.DataFrame = parser.parse_product_list_id(page_number=1)
    context['ti'].xcom_push(key='product_list_df', value=product_list_df)


def parse_urls_of_products(**context):
    """Function that use async-method from AsyncRequester to get urls
    that contains information about personal info of products and their price history
    After that push dataframe with urls to XCOM.
    """
    product_list_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_ID_FROM_PRODUCT_LIST_TASK_ID,
        key='product_list_df'
    )

    if dag_config.IS_BAD_INTERNET:
        product_list_df = product_list_df.head(5)

    async_requester: AsyncRequesterWB = AsyncRequesterWB(product_list_df[postgres_db_constant.PRODUCT_ID])
    urls_df: pandas.DataFrame = async_requester.create_table_with_json_urls()
    context['ti'].xcom_push(key='urls_df', value=urls_df)


def parse_products_personal_info(**context):
    """Function  that parse product personal info by link in urls_df.
    After that push dataframe with urls to XCOM.
    """
    urls_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_URLS_OF_PRODUCTS_TASK_ID,
        key='urls_df'
    )
    product_df: pandas.DataFrame = pandas.DataFrame()

    for product_url in urls_df[postgres_db_constant.PRODUCT_CARD_JSON]:
        product = parser.parse_product(product_url=product_url)
        product_df = pandas.concat([product_df, product])

    context['ti'].xcom_push(key='product_df', value=product_df)


def parse_price_history(**context):
    """Function  that parse product price history by link in urls_df.
    After that push dataframe with urls to XCOM.
    """
    urls_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_URLS_OF_PRODUCTS_TASK_ID,
        key='urls_df'
    )
    price_history_df: pandas.DataFrame = pandas.DataFrame()

    for price_url in urls_df[postgres_db_constant.PRODUCT_PRICE_HISTORY_JSON]:
        price_history = parser.parse_product_price_history(price_url=price_url)
        price_history_df = pandas.concat([price_history_df, price_history])

    context['ti'].xcom_push(key='price_history_df', value=price_history_df)


def parse_feedbacks(**context):
    """Function  that parse product feedbacks.
    After that push dataframe with urls to XCOM.
    """
    product_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_PRODUCTS_PERSONAL_INFO_TASK_ID,
        key='product_df'
    )
    feedback_df: pandas.DataFrame = pandas.DataFrame()

    for product_id, root_id in zip(product_df[postgres_db_constant.PRODUCT_ID],
                                   product_df[postgres_db_constant.ROOT_ID]):
        feedback: pandas.DataFrame = parser.parse_product_feedback(product_id, root_id)
        feedback_df = pandas.concat([feedback_df, feedback])

    context['ti'].xcom_push(key='feedback_df', value=feedback_df)


def upload_new_data_in_products(**context):
    """Function that upload new data in table 'products' in our database.
    """
    product_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_PRODUCTS_PERSONAL_INFO_TASK_ID,
        key='product_df'
    )
    client.update_table_in_db_by_df(df=product_df,
                                    table_name=config.PRODUCT_TABLE,
                                    tmp_table_name=dag_config.TMP_PRODUCT_TABLE_NAME,
                                    is_main_table=True,
                                    data_type=postgres_db_constant.products_table_type_dict)


def upload_new_data_in_urls(**context):
    """Function that upload new data in table 'urls' in our database.
    """
    urls_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_URLS_OF_PRODUCTS_TASK_ID,
        key='urls_df'
    )
    client.update_table_in_db_by_df(df=urls_df,
                                    table_name=config.URLS_TABLE,
                                    tmp_table_name=dag_config.TMP_URLS_TABLE_NAME,
                                    is_main_table=False,
                                    data_type=postgres_db_constant.urls_table_type_dict)


def upload_new_data_in_price_history(**context):
    """Function that upload new data in table 'price_history' in our database.
    """
    price_history_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_PRICE_HISTORY_TASK_ID,
        key='price_history_df'
    )
    client.update_table_in_db_by_df(df=price_history_df,
                                    table_name=config.PRICE_HISTORY_TABLE,
                                    tmp_table_name=dag_config.TMP_PRICE_HISTORY_TABLE_NAME,
                                    is_main_table=False,
                                    data_type=postgres_db_constant.price_history_type_dict)


def upload_new_data_in_feedbacks(**context):
    """Function that upload new data in table 'feedbacks' in our database.
    """
    feedback_df: pandas.DataFrame = context['ti'].xcom_pull(
        task_ids=dag_config.PARSE_FEEDBACKS_TASK_ID,
        key='feedback_df'
    )
    client.update_table_in_db_by_df(df=feedback_df,
                                    table_name=config.FEEDBACKS_TABLE,
                                    tmp_table_name=dag_config.TMP_FEEDBACKS_TABLE_NAME,
                                    is_main_table=False,
                                    data_type=postgres_db_constant.feedbacks_table_type_dict)
