from ..helpers.database import Database
from ..models.atm import Categories, Establishments


class Config:
    def __init__(self):
        self.conn = Database().session()

    def make_migrate(self):
        default_category = Categories(
            name="extras",
            description="Default category maded to receive everything that's not indentified",
            expected=500.00,
        )

        default_establishments = Establishments(
            name="N/A",
            original_name="N/A",
            detail="Used when we don't have info about the establishment",
            is_visible=False,
        )

        self.conn.add(default_category)
        self.conn.add(default_establishments)
        self.conn.commit()
        self.conn.close()
