import arrow
from loguru import logger
from pynubank import Nubank

from monetary_maid.bussines.banks.atm import ATM_API
from monetary_maid.get_env import FOLDER_PATH, PASSWORD, TAX_ID
from monetary_maid.helpers.database import Database

# TODO: criar classe para validação de gastos no Santinhos!!!


class Nubank_API(ATM_API):
    def __init__(self):
        _path = FOLDER_PATH + "cert.p12"
        self.nu = Nubank()
        self.nu.authenticate_with_cert(TAX_ID, PASSWORD, _path)
        self.conn = Database().session()

    def _get_value(self):
        return self.nu.get_account_balance()

    def _get_transactions(self):
        return self.nu.get_account_feed()

    def _get_amount(self, item):
        position = item["detail"].find("$")
        if position >= 0:
            return item["detail"][position + 2 :].replace(".", "").replace(",", ".")
        return 0

    def update_statment(self):
        try:
            transactions = self._get_transactions()
            for item in transactions:
                transaction = {
                    "amount": float(item.get("amount", self._get_amount(item))),
                    "checknum": item["id"],
                    "title": item["title"],
                    "detail": item["detail"],
                    "date": item["postDate"],
                    "typename": item["__typename"],
                }

                self.add_statment(transaction)
                # Valida estabelecimento de compra pra alimentar Establishments
                if transaction["title"] == "Compra no débito":
                    self.add_establishment(
                        transaction["detail"][: transaction["detail"].find("-") - 1]
                    )
        except Exception as error:
            logger.error(error)
