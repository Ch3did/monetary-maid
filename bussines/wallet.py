import arrow

from get_env import PO_BIG_SAVE, PO_INVESTMENT, PO_MONTH_EMERGENCY
from model import FixedDebits, FloatedDebits


class WalletMachine:
    def __init__(self, salary, conn):
        self.session = conn
        self.gross = salary[0]
        self.fixed_debits_details = dict(self._get_fixed_debits())
        self.floated_debits_details = dict(self._get_floated_debits())
        self.fixed_debits = self._sum(self.fixed_debits_details)
        self.floated_debits = self._sum(self.floated_debits_details)
        self.net = self.gross - self.fixed_debits - self.floated_debits
        self.invest = self.net * float(PO_INVESTMENT)
        self.big_save = self.net * float(PO_BIG_SAVE)
        self.month_emergency = self.net * float(PO_MONTH_EMERGENCY)
        self.available = self.net - self.invest - self.big_save - self.month_emergency
        self.time_stamp = arrow.now().format("YYYY-MM-DD")
        self.date = arrow.now().strftime("%Y-%m")

    def _get_fixed_debits(self):
        if (
            fix_debts := self.session.query(FixedDebits.name, FixedDebits.amount)
            .filter_by(use=True)
            .all()
        ):
            return fix_debts
        return {}

    def _get_floated_debits(self):
        if (
            floated_debits := self.session.query(
                FloatedDebits.name, FloatedDebits.amount
            )
            .filter_by(use=True)
            .all()
        ):
            return floated_debits
        return {}

    def _sum(self, debits):
        sum = 0
        for debit in debits:
            sum += float(debits[debit])
        return sum
