"""Global file with constants for all project.
"""

import os

NULL_VALUE = None

POSTGRES_USERNAME: str = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD: str = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB_NAME: str = os.environ.get('POSTGRES_DB')
POSTGRES_HOST: str = "postgres"

PRODUCT_TABLE: str = "products"

PRICE_HISTORY_TABLE: str = "price_history"
PRICE_TABLE: str = "price"

FEEDBACKS_TABLE: str = "feedbacks"
GRADE_TABLE: str = "grade"
GRADE_HISTORY_TABLE: str = "grade_history"

URLS_TABLE: str = "urls"
