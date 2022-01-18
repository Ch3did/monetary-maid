import json

import arrow
from loguru import logger

from bussines.helpers.args import get_args
from bussines.helpers.database import Database
from bussines.helpers.func import sum_dict
from bussines.wallet import WalletMachine
from model import Wallet

args = get_args()


class CLI:
    def __init__(self):
        self.conn = Database().session()

    def _validate_date(self):
        if arrow.get(
            self.conn.query(Wallet.date).order_by(Wallet.date.desc()).first()[0]
        ).strftime("%m-%Y") == arrow.now().strftime("%m-%Y"):
            return False
        return True

    def register_month_salary(self):
        if not self._validate_date():
            return logger.error(
                "You can't register a new month salary, because you already registered one."
            )
        try:
            logger.info(f"Salary: {args.amount}")

            machine = WalletMachine(args.amount, self.conn)

            wallet = Wallet(
                gross=machine.gross,
                fixed_debits=machine.fixed_debits,
                floated_debits=machine.floated_debits,
                net=machine.net,
                invest=machine.invest,
                big_save=machine.big_save,
                month_emergency=machine.month_emergency,
                available=machine.available,
                date=machine.date,
                debits_details=sum_dict(
                    machine.fixed_debits_details, machine.floated_debits_details
                ),
            )
            self.conn.session.add(wallet)
            self.conn.session.commit()
            logger.info(f"Your Wallet is saved!")
            logger.info(f"Net: R${machine.net:.2f}")
            logger.info(f"Invest: R${machine.invest:.2f}")
            logger.info(f"Big Save: R${machine.big_save:.2f}")
            logger.info(f"Month Emergency: R${machine.month_emergency:.2f}")
            logger.info(f"Available: R${machine.available:.2f}")
        except Exception as e:
            logger.error(f"{e}")


# TODO: Make more CLI functions

if __name__ == "__main__":
    cli = CLI()
    cli.register_month_salary()

# TODO: Criar meio de popular a tabela
