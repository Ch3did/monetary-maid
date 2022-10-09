from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.get_env import DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER, DEBUG


class Database:
    def __init__(self):
        self.engine = create_engine(self._make_endpoint(), echo=bool(DEBUG))
        self.session = self.make_session()

    def _make_endpoint(self):
        return f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    def make_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session
