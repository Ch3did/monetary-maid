import arrow

from monetary_maid.get_env import PO_BIG_SAVE, PO_INVESTMENT, PO_MONTH_EMERGENCY
from monetary_maid.helpers.database import Database
from monetary_maid.helpers.func import sum_dict
from monetary_maid.model import FixedDebits, FloatedDebits, Wallet


class WalletMachine:
    @classmethod
    def _sum(cls, debits):
        sum = 0
        for debit in debits:
            sum += float(debits[debit])
        return sum

    def _get_fixed_debits(self):
        session = Database.session()
        fix_debts = (
            session.query(FixedDebits.name, FixedDebits.amount)
            .filter_by(use=True)
            .all()
        )
        session.close()
        if fix_debts:
            return fix_debts
        return {}

    def _get_floated_debits(self):
        session = Database.session()
        floated_debits = (
            session.query(FloatedDebits.name, FloatedDebits.amount)
            .filter_by(use=True)
            .all()
        )
        session.close()
        if floated_debits:
            return floated_debits
        return {}

    def save_new_wallet(self, salary):
        gross = salary
        fixed_debits_details = dict(self._get_fixed_debits())
        floated_debits_details = dict(self._get_floated_debits())
        fixed_debits = self._sum(self.fixed_debits_details)
        floated_debits = self._sum(self.floated_debits_details)
        net = gross - fixed_debits - floated_debits
        invest = net * float(PO_INVESTMENT)
        big_save = net * float(PO_BIG_SAVE)
        month_emergency = net * float(PO_MONTH_EMERGENCY)
        available = net - invest - big_save - month_emergency
        time_stamp = arrow.now().format("YYYY-MM-DD")
        date = arrow.now().strftime("%Y-%m")

        wallet = Wallet(
            gross=gross,
            fixed_debits=fixed_debits,
            floated_debits=floated_debits,
            net=net,
            invest=invest,
            big_save=big_save,
            month_emergency=month_emergency,
            available=available,
            timestamp=time_stamp,
            date=date,
            debits_details=sum_dict(fixed_debits_details, floated_debits_details),
        )

        session = Database().session()
        session.add(wallet)
        session.commit()
        session.close()

        return wallet
