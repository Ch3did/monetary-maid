import arrow
from loguru import logger
from pynubank import Nubank

from src.bussines.atm import Statment_ATM
from src.get_env import FOLDER_PATH, PASSWORD, TAX_ID
from src.helpers.database import Database

# TODO: criar classe para validação de gastos no Santinhos!!!


class Nubank_API(Statment_ATM):
    def __init__(self):
        _path = FOLDER_PATH + "cert.p12"
        self.nu = Nubank()
        self.nu.authenticate_with_cert(TAX_ID, PASSWORD, _path)
        self.conn = Database().session()

    def _get_value(self):
        return self.nu.get_account_statements()

    def _get_transactions(self):
        return self.nu.get_account_statements()

    def _update_relations(self, type, detail):
        id_establishment = 1
        id_type = self._add_type(type)
        if detail.find("R$") > 0:
            position = detail.find("R$")
            id_establishment = self._add_establishment(
                (detail[:position]).lstrip(" ").rstrip(".- ").capitalize()
            )

        # TODO: Setar valor default para establishment == None

        return {"type_id": id_type, "establishment_id": id_establishment}

    def _get_amount(self, item):
        position = item["detail"].find("$")
        if position >= 0:
            return item["detail"][position + 2 :].replace(".", "").replace(",", ".")
        return 0

    def update_statment(self):
        try:
            transactions = self._get_transactions()
            for item in transactions:
                # Formata dados recebidos para análise
                transaction = {
                    "amount": float(item.get("amount", self._get_amount(item))),
                    "checknum": item["id"],
                    "title": item["title"],
                    "detail": item["detail"],
                    "date": item["postDate"],
                    "typename": item["__typename"],
                }
                relation_values = self._update_relations(
                    transaction["title"], transaction["detail"]
                )
                transaction["type_id"] = relation_values["type_id"]
                transaction["establishment_id"] = relation_values["establishment_id"]

                self._add_statment(transaction)
                # Valida estabelecimento de compra pra alimentar Establishments

        except Exception as error:
            logger.error(error)
