import arrow
from loguru import logger
from pynubank import Nubank

from src.bussines.atm import Statment_ATM
from src.get_env import FOLDER_PATH, PASSWORD, TAX_ID
from src.helpers.database import Database


class Nubank_API(Statment_ATM):
    def __init__(self):
        _path = FOLDER_PATH + "cert.p12"
        self.nu = Nubank()
        self.nu.authenticate_with_cert(TAX_ID, PASSWORD, _path)
        self.conn = Database().session()

    @staticmethod
    def _find_establishment_name(original_name):
        return original_name[:position].lower().rstrip().strip("-").rstrip().lstrip()
        # else:
        return "n/a"

    def _get_debit_statments(self):
        return self.nu.get_account_statements()

    def _get_credit_statments(self):
        return self.nu.get_card_statements()

    def _get_card_detail(self, transaction):
        return self.nu.get_card_statement_details(transaction)

    def _update_relations(self, relation):
        """sanatizar nomes e informações nessa camada"""
        response = {}

        if relation.get("transaction_type"):
            response["id_type"] = self._add_type(relation["transaction_type"])

        position = relation["establishment"]["original_name"].find("R$")
        relation["establishment"]["sanatize_original_name"] = relation["establishment"][
            "original_name"
        ][:position].lower()

        if not relation["establishment"].get("name"):
            relation["establishment"]["name"] = (
                relation["establishment"]["sanatize_original_name"]
                .rstrip()
                .strip("-")
                .strip("\n")
                .rstrip()
                .lstrip()
            )

            relation["establishment"]["mcc"] = None
            relation["establishment"]["country"] = "brasil"

        relation["establishment"]["original_name"] = (
            relation["establishment"]["original_name"].strip("-").rstrip().lstrip()
        )

        response["id_establishment"] = self._add_establishment(
            relation["establishment"]
        )

        return {
            "type_id": response.get("id_type", None),
            "establishment_id": response.get("id_establishment", None),
        }

    def _get_amount(self, item):
        position = item["detail"].find("$")
        if position >= 0:
            return item["detail"][position + 2 :].replace(".", "").replace(",", ".")
        return 0

    def _credit_update(self):
        try:
            transactions = self._get_credit_statments()
            for item in transactions:
                if item_detail := self._get_card_detail(item).get("transaction"):
                    relation = {
                        "establishment": {
                            "original_name": item_detail["original_merchant_name"],
                            "name": item_detail["merchant_name"].lower().rstrip(),
                            "mcc": item_detail["mcc"],
                            "date": item_detail["time"],
                            "country": item_detail["country"].lower().rstrip(),
                        }
                    }
                    relation_values = self._update_relations(relation)

                    for detail in item_detail["charges_list"]:
                        transaction = {
                            "checknum": item["id"],
                            "category": item["category"],
                            "total_amount": item["amount"],
                            "instalment_amount": detail["amount"],
                            "status": detail["status"],
                            "instalment_date": detail["post_date"],
                            "instalment_index": detail["index"] + 1,
                            "instalment_promotion_reason": detail.get(
                                "promotion_reason", None
                            ),
                            "purchase_date": item["time"],
                            "title": item["title"],
                            "source": item["source"],
                            "card_last_digits": item_detail["card_last_four_digits"],
                            "card_type": item_detail["card_type"],
                            "amount_without_iof": item_detail["amount_without_iof"],
                            "card_id": item_detail["card"],
                            "event_type": item_detail["event_type"],
                            "establishment_id": relation_values["establishment_id"],
                        }

                        self._add_credit_statment(transaction)
                else:
                    logger.error(
                        "____________________________________________________  tA ERRADO ISSO, ARRUMA"
                    )

        except Exception as error:
            logger.error(error)

    def _debit_update(self):
        try:
            transactions = self._get_debit_statments()
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

                relation = {
                    "establishment": {
                        "original_name": transaction["detail"],
                        "date": transaction["date"],
                    },
                    "transaction_type": transaction["title"],
                }

                relation_values = self._update_relations(relation)

                transaction["type_id"] = relation_values["type_id"]
                transaction["establishment_id"] = relation_values["establishment_id"]

                self._add_statment(transaction)
                # Valida estabelecimento de compra pra alimentar Establishments

        except Exception as error:
            logger.error(error)

    def update_statment(self):
        # self._debit_update()
        self._credit_update()
