import arrow
from pynubank import Nubank

from bussines.helpers.database import Database
from get_env import FOLDER_PATH, PASSWORD, TAX_ID
from model import NubankModel


class Nubank_API(Nubank):
    def login(self):
        _path = FOLDER_PATH + "cert.p12"
        self.authenticate_with_cert(TAX_ID, PASSWORD, _path)
        self.conn = Database().session()

    def _get_value(self):
        return self.get_account_balance()

    def _get_transactions(self):
        return self.get_account_feed()

    def _get_amount(self, item):
        position = item["detail"].find("$")
        if position >= 0:
            return item["detail"][position + 2 :].replace(".", "").replace(",", ".")
        return 0

    def update_statment(self):
        last_date = (
            self.conn.query(NubankModel.date)
            .order_by(NubankModel.date.desc())
            .first()["date"]
        )
        last_register = (
            self.conn.query(NubankModel.checknum)
            .filter(NubankModel.date == last_date)
            .all()
        )
        transactions = self._get_transactions()
        last_date = arrow.get(last_date)
        for item in transactions:
            if (
                not item["id"] in last_register[0]
                and arrow.get(item["postDate"]) >= last_date
            ):
                value = item.get("amount", self._get_amount(item))
                nu = NubankModel(
                    checknum=item["id"],
                    title=item["title"],
                    detail=item["detail"],
                    date=item["postDate"],
                    typename=item["__typename"],
                    amount=float(value),
                )
                self.conn.add(nu)
                self.conn.commit()
                print(f"inserido no banco, {value}")
        self.conn.close()
