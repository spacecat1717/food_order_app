import os

from dotenv import load_dotenv

load_dotenv()

PSQL_DB = os.getenv('PSQL_DB')
PSQL_USER = os.getenv('PSQL_USER')
PSQL_PASS = os.getenv('PSQL_PASS')
PSQL_HOST = os.getenv('PSQL_HOST')

DATABASE_URL = f'postgresql+asyncpg://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}/{PSQL_DB}'
