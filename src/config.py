"""Global file with constants for all project.
"""

import os

PATH_TO_BROWSER = os.environ.get('ChromePath')

NULL_VALUE = None

POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB_NAME = os.environ.get('POSTGRES_DB')
POSTGRES_HOST = "postgres"

PRICE_HISTORY_TABLE = "price_history"
PRICE_TABLE = "price"

FEEDBACKS_TABLE = "feedbacks"
GRADE_TABLE = "grade"