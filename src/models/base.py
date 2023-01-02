from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

from src.get_env import SCHEMA

# metadata_obj = MetaData(schema=SCHEMA)


Base = declarative_base()  # metadata=metadata_obj)
