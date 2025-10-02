# > pip install Flask-SQLAlchemy psycopg2-binary

import os

DB_USER = os.environ.get('POSTGRES_USER')
DB_PASSWORD = os.environ.get('POSTGRES_PASS_RDS')
DB_HOST = 'django-pgs.cmivhxqxeajf.us-east-2.rds.amazonaws.com'
DB_NAME = 'initialdb'
DB_PORT = 5432

DB_URLSTRING = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
