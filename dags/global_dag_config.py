"""File with global constant values for DAGs.
"""
from datetime import datetime

from src.database.IClient import IClient
from src.database.postgres.ClientPostgres import ClientPostgres
from src.database.postgres.ConnectorPostgres import ConnectorPostgres
from src.parser.IParser import IParser
from src.parser.WB.ParserWB import ParserWB

# Instance of IClient.
client: IClient = ClientPostgres(ConnectorPostgres())

# Instance of IParser.
parser: IParser = ParserWB()

# Current date in format YYYY_MM_DD.
CURRENT_DATE_YYYY_MM_DD: str = datetime.now().strftime('%Y_%m_%d')

# Airflow schema name in database.
AIRFLOW_DB_SCHEMA: str = "airflow"

"""XCOM constants.
"""
XCOM_TABLE_NAME: str = "xcom"
XCOM_DAG_ID_COLUMN: str = "dag_id"

"""DAGs IDs.
"""
CREATE_PRICE_TABLE_DAG_ID: str = "create-price-table"
CREATE_GRADE_TABLE_DAG_ID: str = "create-grade-table"
UPDATE_GRADE_HISTORY_TABLE_DAG_ID: str = "update-grade-history"
UPDATE_PRICE_HISTORY_TABLE_DAG_ID: str = "update-price-history"
UPDATE_FEEDBACKS_TABLE_DAG_ID: str = "update-feedbacks"
UPDATE_PRODUCTS_TABLE_DAG_ID: str = "update-products"
ADD_PRODUCT_IN_TABLE_DAG_ID: str = "add-products"
REMOVE_PRODUCTS_FROM_DATABASE_DAG_ID: str = "remove-products"

"""Task IDs
"""
CLEAR_XCOM_CACHE_TASK_ID: str = "clear_xcom_cache"
CLOSE_CONNECTION_TASK_ID: str = "close_connection"
SORT_DATA_IN_TABLE_TASK_ID: str = "sort_data_in_table"

"""Daily DAGs parameters
"""
DAILY_ADD_DAG_PARAMETERS: dict = {
    "schedule_interval": "@daily",
    "max_active_runs": 1,
    "tags": ["add"]
}

DAILY_CREATE_DAG_PARAMETERS: dict = {
    "schedule_interval": "@daily",
    "max_active_runs": 1,
    "tags": ["create"]
}

DAILY_REMOVE_DAG_PARAMETERS: dict = {
    "schedule_interval": "@daily",
    "max_active_runs": 1,
    "tags": ["remove"]
}

DAILY_UPDATE_DAG_PARAMETERS: dict = {
    "schedule_interval": "@daily",
    "max_active_runs": 1,
    "tags": ["update"]
}

"""Sensors parameters
"""
DEFAULT_SENSORS_PARAMETERS: dict = {
    "external_task_id": None,
    "poke_interval": 60,  # 1 minute
    "timeout": 60 * 60,  # 1 hour
}