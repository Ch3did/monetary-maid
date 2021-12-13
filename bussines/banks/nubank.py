from pynubank import Nubank
from get_env import TAX_ID, PASSWORD, FOLDER_PATH


class Nubank():
    def __init__(self):
        self.nubank = Nubank()

    def login(self):
        self.nubank.authenticate_with_cert(TAX_ID, PASSWORD, FOLDER_PATH)

    def _get_value(self):
        return self.get_account_balance()

    def _get_transactions(self):
        return self.nubank.get_account_feed()

    @staticmethod
    def calculate_bank_values(self):
        valor = self._get_value()
        transactions = self._get_transactions()
        