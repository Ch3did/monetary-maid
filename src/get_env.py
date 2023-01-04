import os

from dotenv import load_dotenv

load_dotenv("monetary_maid.config")

DEBUG = os.environ.get("DEBUG")

# Nubank Data
TAX_ID = os.environ.get("TAX_ID")
PASSWORD = os.environ.get("PASSWORD")
FOLDER_PATH = os.environ.get("FOLDER_PATH")


# DB Conection
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")

SCHEMA = os.environ.get("SCHEMA")

USER_NAME = os.environ.get("USER_NAME")
