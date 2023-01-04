from src.helpers.database import Database
from src.helpers.exception import ATMException
from src.models.categories import Categories


class Category_ATM:
    def __init__(self):

        self.conn = Database().session()

    def add_category(self, name, description, expected):
        if (
            self.conn.query(Categories.id)
            .filter(Categories.name == name.rstrip())
            .first()
        ):
            raise ATMException(
                message="Category already exists... ",
                description=description,
                expected=expected,
            )
        category = Categories(
            name=name, description=description, expected=expected, is_visible=True
        )

        if float(expected) < 0:
            Categories.is_spend = True

        self.conn.add(category)
        self.conn.commit()
        self.conn.close()

    def get_categories_list(self, search_type):
        if int(search_type) == 1:  # VISIBLE
            return (
                self.conn.query(Categories).filter(Categories.is_visible == True).all()
            )
        if int(search_type) == 0:  # ALL
            return self.conn.query(Categories).all()
        else:
            return [
                self.conn.query(Categories).filter(Categories.id == search_type).first()
            ]
