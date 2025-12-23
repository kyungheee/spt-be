import psycopg2
from datetime import datetime, date
import pytz
import os
from env_var import REGISTERED_IDS
from dotenv import load_dotenv

DB_CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": os.getenv("POSTGRES_HOST"),
    "port": int(os.getenv("POSTGRES_PORT", 5432))
}