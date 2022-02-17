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

    def get_money_info(self, month=arrow.now().strftime("%Y-%m")):
        try:
            if wallet := self.conn.query(Wallet).filter(Wallet.date == month).first():
                logger.info(f"Gross: R${wallet.gross:.2f}")
                logger.info(f"Net: R${wallet.net:.2f}")
                logger.info(f"Invest: R${wallet.invest:.2f}")
                logger.info(f"Big Save: R${wallet.big_save:.2f}")
                logger.info(f"Month Emergency: R${wallet.month_emergency:.2f}")
                logger.info(f"Available: R${wallet.available:.2f}")
                logger.info(f"Timestamp: {wallet.timestamp}")
            else:
                logger.error(f"You don't have a wallet for {month}")
        except Exception as e:
            logger.error(f"{e}")

    def get_debits_info(self):
        try:
            wallet = self.conn.query(Wallet).order_by(Wallet.id.desc()).first()
            for key in  wallet.debits_details:
                logger.info({key: wallet.debits_details[key]})
            logger.info(f" -   Fixed Debits: R${wallet.fixed_debits:.2f}")
            logger.info(f" -   Floated Debits: R${wallet.floated_debits:.2f}")
        except Exception as e:
            logger.error(f"{e}")

    def _validate_date(self):
        if (
            last_date := self.conn.query(Wallet.date)
            .order_by(Wallet.date.desc())
            .first()
        ):
            if arrow.get(last_date[0]).strftime("%m-%Y") == arrow.now().strftime(
                "%m-%Y"
            ):
                return False
        return True

    def register_month_salary(self):
        if not self._validate_date():
            return logger.error(
                "You can't register a new month salary, because you already registered one."
            )
        try:
            logger.info(f"Salary: {args.get('register')[0]}")

            machine = WalletMachine(args["register"], self.conn)

            wallet = Wallet(
                gross=machine.gross,
                fixed_debits=machine.fixed_debits,
                floated_debits=machine.floated_debits,
                net=machine.net,
                invest=machine.invest,
                big_save=machine.big_save,
                month_emergency=machine.month_emergency,
                available=machine.available,
                timestamp=machine.time_stamp,
                date=machine.date,
                debits_details=sum_dict(
                    machine.fixed_debits_details, machine.floated_debits_details
                ),
            )
            self.conn.add(wallet)
            self.conn.commit()
            logger.info(f"Your Wallet is saved!")
            total = float(machine.floated_debits) + float(machine.fixed_debits)
            logger.info(f"Bills: R${total:.2f}")
            logger.info(f"Net: R${machine.net:.2f}")
            logger.info(f"Invest: R${machine.invest:.2f}")
            logger.info(f"Big Save: R${machine.big_save:.2f}")
            logger.info(f"Month Emergency: R${machine.month_emergency:.2f}")
            logger.info(f"Available: R${machine.available:.2f}")
        except Exception as e:
            logger.error(f"{e}")


if __name__ == "__main__":
    c = CLI()
    if args["get"]:
        if not args['period']:
            c.get_money_info()
        else:
            c.get_money_info(args['period'][0])
            
    elif args["register"]:
        c.register_month_salary()
    elif args["debits"]:
        c.get_debits_info()
    else:
        logger.error("You need to specify a option")
