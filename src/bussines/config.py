from src.models.base import Base
from src.models.categories import Categories

from ..helpers.database import Database

# from src.get_env import SCHEMA


class Config:
    def __init__(self):
        db = Database()
        self.conn = db.session()
        self.engine = db.engine

    def make_migrate(self):
        Base.metadata.create_all(self.engine)
        self.conn.commit()

        default_category = Categories(
            name="invisible",
            description="Default category maded to receive everything that's not indentified",
            expected=500.00,
            is_visible=False,
        )

        self.conn.add(default_category)
        self.conn.commit()
        self.conn.close()
