from models.fixed_debits import FixedDebits
from models.floated_debits import FloatedDebits
from get_env import PO_INVESTMENT, PO_BIG_SAVE


class Prepare_salary:
    
    def _calculate_percentage(self):
        self.invest = self.salary * PO_INVESTMENT
        self.net = self.gross - self._get_fixed_debits()- self._get_floated_debits()
        self.porcent_big_save = self.net * PO_BIG_SAVE
    
    def _get_fixed_debits(self):
        fixed = FixedDebits()
    
    def _get_floated_debits(self):
        floated = FloatedDebits()
    
    @staticmethod
    def run(self, salary):
        self.gross = salary
        self._calculate_percentage()
