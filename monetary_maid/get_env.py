import os

from dotenv import load_dotenv

# Nubank Data
# TAX_ID=os.environ.get['TAX_ID']
# PASSWORD=os.environ.get['PASSWORD']
# FOLDER_PATH=os.environ.get['FOLDER_PATH']

load_dotenv("monetary_maid.config")

DEBUG = os.environ.get("DEBUG")

# Nubank Data
TAX_ID = os.environ.get("TAX_ID")
PASSWORD = os.environ.get("PASSWORD")
FOLDER_PATH = os.environ.get("FOLDER_PATH")

# PLR
PO_INVESTMENT = os.environ.get("PO_INVESTMENT")
PO_BIG_SAVE = os.environ.get("PO_BIG_SAVE")
PO_MONTH_EMERGENCY = os.environ.get("PO_MONTH_EMERGENCY")

# DB Conection
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
