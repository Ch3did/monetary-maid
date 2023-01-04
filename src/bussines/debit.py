import arrow
from loguru import logger

from src.helpers.database import Database
from src.helpers.exception import ATMException
from src.models.categories import Categories
from src.models.debit import Debit


class Debit_ATM:
    def __init__(self):
        self.conn = Database().session()

    # Add

    def _add_debit(self, item):
        if not (
            self.conn.query(Debit)
            .filter(Debit.checknum == item["checknum"])
            .filter(Debit.detail == item["detail"])
            .filter(Debit.date == item["date"])
            .filter(Debit.establishment == item["establishment"])
            .filter(Debit.typename == item["typename"])
            .filter(Debit.amount == item["amount"])
            .filter(Debit.is_negative == item["is_negative"])
            .all()
        ):
            transaction = Debit(
                checknum=item["checknum"],
                detail=item["detail"],
                date=item["date"],
                typename=item["typename"],
                amount=item["amount"],
                establishment=item["establishment"],
                is_negative=item["is_negative"],
                category=1,
            )

            self.conn.add(transaction)
            logger.info(f"inserido no banco: {item['title']}")
            self.conn.commit()
            self.conn.close()

    # Get

    def get_debits(self, period=arrow.now().shift(days=-4).format("YYYY-MM-01")):
        return (
            self.conn.query(Debit, Categories)
            .join(Categories, Debit.category == Categories.id)
            .filter(Debit.date >= period)
            .all()
        )

    def get_debit(self, id):
        return self.conn.query(Debit).filter(Debit.id == id).first()

    def get_debit_by_id(self, id):
        return (
            self.conn.query(Debit, Categories)
            .join(Categories, Debit.category == Categories.id)
            .filter(Debit.id == id)
            .first()
        )

    # Update

    def update_debits_category(self, debit_id, category_id):
        if self.conn.query(Debit.id).filter(Debit.id == debit_id).all():
            self.conn.query(Debit).filter(Debit.id == debit_id).update(
                {
                    Debit.category: f"{category_id}",
                }
            )
            self.conn.commit()
            self.conn.close()
        else:
            raise ATMException(message="Debit ID Not Found")
