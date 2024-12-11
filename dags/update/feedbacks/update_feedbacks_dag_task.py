import pandas

from src import config
from src.database.postgres import postgres_db_constant

from dags.global_dag_config import client, parser
from dags.update.feedbacks import update_feedbacks_dag_config as dag_config


def get_root_and_product_ids_from_table_products(**context):
    """Function that getting root_id and product_id
    from table 'products'.
    After that push this like dataframe in XCOM.
    """
    id_df: pandas.DataFrame = client.create_dataframe_by_sql(
        query=dag_config.SELECT_IDS_FROM_TABLE_PRODUCTS_QUERY
    )

    context['ti'].xcom_push(key="id_df", value=id_df)


def find_update_for_feedbacks(**context):
    """Function that parse feedbacks for every product.
    After that push dataframe with new data of feedbacks in XCOM.
    """
    id_df: pandas.DataFrame = context['ti'].xcom_pull(
        key="id_df",
        task_ids=dag_config.GET_ROOT_AND_PRODUCT_IDS_FROM_TABLE_PRODUCTS_TASK_ID
    )

    feedbacks_df: pandas.DataFrame = pandas.DataFrame()

    for root_id, product_id in zip(id_df[postgres_db_constant.ROOT_ID],
                                   id_df[postgres_db_constant.PRODUCT_ID]):
        feedback: pandas.DataFrame = parser.parse_product_feedback(product_id, root_id)
        feedbacks_df = pandas.concat([feedbacks_df, feedback])

    context['ti'].xcom_push(key="feedbacks_df",
                            value=feedbacks_df)


def upload_updated_data_to_table(**context):
    """Function that upload new data in table 'feedbacks' in our database
    """
    feedbacks_df: pandas.DataFrame = context['ti'].xcom_pull(
        key="feedbacks_df",
        task_ids=dag_config.FIND_UPDATE_FOR_FEEDBACKS_TASK_ID
    )

    client.update_table_in_db_by_df(df=feedbacks_df,
                                    table_name=config.FEEDBACKS_TABLE,
                                    tmp_table_name=dag_config.TMP_FEEDBACKS_TABLE_NAME,
                                    is_main_table=False,
                                    data_type=postgres_db_constant.feedbacks_table_type_dict)
