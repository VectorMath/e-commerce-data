"""Global file with constants for all project.
"""

import os

PATH_TO_BROWSER = os.environ.get('ChromePath')

NULL_VALUE = None

POSTGRES_USERNAME = os.environ.get('POSTGRES_USERNAME')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_DB_NAME = os.environ.get('DATABASE_NAME')
POSTGRES_HOST = "localhost"