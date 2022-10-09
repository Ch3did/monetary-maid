from ..helpers.database import Database
from ..models.atm import Categories


class Config:
    def __init__(self):
        self.conn = Database().session()


def make_migrate(self):
    default = Categories(
        name="Extras",
        description="Default category maded to receive everything that's not indentified",
        expected=500.00,
        upated_at=None,
    )

    self.conn.add(default)
    self.conn.commit()
    self.conn.close()
