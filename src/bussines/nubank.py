import arrow
from loguru import logger
from pynubank import Nubank

from src.bussines.debit import Debit_ATM
from src.get_env import FOLDER_PATH, PASSWORD, TAX_ID
from src.helpers.database import Database


class Nubank_API(Debit_ATM):
    def __init__(self):
        _path = FOLDER_PATH + "cert.p12"
        self.nu = Nubank()
        self.nu.authenticate_with_cert(TAX_ID, PASSWORD, _path)
        self.conn = Database().session()
        self.cash_in = [
            "PixTransferInEvent",
            "DebitPurchaseReversalEvent",
        ]

        self.cash_out = [
            "DebitWithdrawalEvent",
            "TransferOutEvent",
            "PixTransferOutEvent",
            "PixTransferScheduledEvent",
            "BarcodePaymentEvent",
            "BillPaymentEvent",
            "DebitPurchaseEvent",
        ]
        self.ignore = ["PixTransferFailedEvent"]

    # Get debit list
    def _get_debit_statments(self):
        return self.nu.get_account_statements()

    def _validate_signal(self, typename):
        if typename in self.cash_in:
            return False
        elif typename in self.cash_out:
            return True
        else:
            raise Exception

    def _get_amount(self, item):
        position = item["detail"].find("$")
        if position >= 0:
            return float(
                item["detail"][position + 2 :].replace(".", "").replace(",", ".")
            )
        return 0

    def update(self):
        try:
            transactions = self._get_debit_statments()
            for item in transactions:
                if item["__typename"] not in self.ignore:
                    # Formata dados recebidos para insert
                    removed_point = item["detail"].find("R$")
                    establishment = (
                        item["detail"][:removed_point]
                        .lower()
                        .rstrip()
                        .strip("-")
                        .strip("\n")
                        .rstrip()
                        .lstrip()
                    )
                    transaction = {
                        "amount": item.get("amount", self._get_amount(item)),
                        "checknum": item["id"],
                        "title": item["title"],
                        "detail": item["detail"].upper(),
                        "establishment": establishment,
                        "date": item["postDate"],
                        "typename": item["__typename"],
                        "is_negative": self._validate_signal(item["__typename"]),
                    }

                    self._add_debit(transaction)

        except Exception as error:
            logger.error(error)
