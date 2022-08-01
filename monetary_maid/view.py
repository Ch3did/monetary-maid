import json

import arrow
from loguru import logger

from monetary_maid.bussines.wallet import WalletMachine


def get_wallet_info(period=arrow.now().strftime("%Y-%m")):
    try:
        if wallet := WalletMachine().get_wallet(period):
            logger.info(wallet)
            # logger.info(f"Gross: R${wallet.gross:.2f}")
            # logger.info(f"Net: R${wallet.net:.2f}")
            # logger.info(f"Invest: R${wallet.invest:.2f}")
            # logger.info(f"Big Save: R${wallet.big_save:.2f}")
            # logger.info(f"Month Emergency: R${wallet.month_emergency:.2f}")
            # logger.info(f"Available: R${wallet.available:.2f}")
            # logger.info(f"Timestamp: {wallet.timestamp}")
        else:
            logger.error(f"You don't have a wallet for {period}")
    except Exception as e:
        logger.error(f"{e}")


def get_debits_info():
    try:
        if wallet := WalletMachine().get_debit():
            for key in wallet.debits_details:
                logger.info({key: wallet.debits_details[key]})
            logger.info(f" -   Fixed Debits: R${wallet.fixed_debits:.2f}")
            logger.info(f" -   Floated Debits: R${wallet.floated_debits:.2f}")
    except Exception as e:
        logger.error(f"{e}")


def register_month_salary(salary):
    # if not self._validate_date():
    #     return logger.error(
    #         "You can't register a new month salary, because you already registered one."
    #     )
    try:
        wallet = WalletMachine().save_new_wallet(salary)
        logger.info(f"Your Wallet is saved!")
        total = float(wallet.floated_debits) + float(wallet.fixed_debits)
        logger.info(f"Bills: R${total:.2f}")
        logger.info(f"Net: R${wallet.net:.2f}")
        logger.info(f"Invest: R${wallet.invest:.2f}")
        logger.info(f"Big Save: R${wallet.big_save:.2f}")
        logger.info(f"Month Emergency: R${wallet.month_emergency:.2f}")
        logger.info(f"Available: R${wallet.available:.2f}")
    except Exception as e:
        logger.error(f"{e}")


def register_debit():
    pass


# def _validate_date():
#     if (
#         last_date := conn.query(Wallet.date)
#         .order_by(Wallet.date.desc())
#         .first()
#     ):
#         if arrow.get(last_date[0]).strftime("%m-%Y") == arrow.now().strftime(
#             "%m-%Y"
#         ):
#             return False
#     return True
