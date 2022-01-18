import arrow

from get_env import PO_BIG_SAVE, PO_INVESTMENT, PO_MONTH_EMERGENCY
from model import FixedDebits, FloatedDebits


class WalletMachine:
    def __init__(self, salary, conn):
        self.session = conn
        self.gross = salary[0]
        self.fixed_debits_details = self._to_dict(self._get_fixed_debits())
        self.floated_debits_details = self._to_dict(self._get_floated_debits())
        self.fixed_debits = self._sum(self.fixed_debits_details)
        self.floated_debits = self._sum(self.floated_debits_details)
        self.net = self.gross - self.fixed_debits - self.floated_debits
        self.invest = self.net * float(PO_INVESTMENT)
        self.big_save = self.net * float(PO_BIG_SAVE)
        self.month_emergency = self.net * float(PO_MONTH_EMERGENCY)
        self.available = self.net - self.invest - self.big_save - self.month_emergency
        self.date = arrow.now().format("YYYY-MM-DD")

    def _get_fixed_debits(self):
        return (
            self.session.query(FixedDebits.name, FixedDebits.amount)
            .filter_by(use=True)
            .all()
        )

    def _get_floated_debits(self):
        return (
            self.session.query(FloatedDebits.name, FloatedDebits.amount)
            .filter_by(use=True)
            .all()
        )

    def _to_dict(self, query):
        new_struckt = {}
        for item in query:
            new_struckt[item[0]] = item[1]
        return new_struckt

    def _sum(self, debits):
        sum = 0
        for debit in debits:
            sum += float(debits[debit])
        return sum
