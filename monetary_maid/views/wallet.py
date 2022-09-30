import arrow
from loguru import logger

from monetary_maid.bussines.wallet import WalletMachine
from monetary_maid.helpers.validators import (
    is_amount_valid,
    is_date_valid,
    is_name_valid,
    is_payment_day_valid,
)

# TODO: Colocar pra funcionar todas as funções


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
            logger.info(f"Fixed Debits: R${wallet.fixed_debits:.2f}")
            logger.info(f"Floated Debits: R${wallet.floated_debits:.2f}")
    except Exception as e:
        logger.error(f"{e}")


def register_month_salary():
    try:
        salary = input("Salary: ")
        wallet = WalletMachine().save_wallet(salary)
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


def register_debit(instalments="", due_instalment=""):
    try:
        name = input("Name: ")
        description = input("Description: ")
        validator = "Amount"
        if amount := is_amount_valid(input("Amount (%.2): ")):
            validator = "Start Date & End Date"
            if dates := is_date_valid(
                input("Start Date (YYYY-MM-DD): "), input("End Date (YYYY-MM-DD): ")
            ):
                validator = "Payment Day"
                if payment_day := is_payment_day_valid(input("Payment Day: ")):
                    use = bool(input("Use (True or leve it blank): "))
                    if bool(input("Is a floated debit? (Yes or leve it blank) ")):
                        instalments = input("How many instalments? ")
                        due_instalment = input("Which instalment is due? ")

                    WalletMachine().save_debit(
                        name,
                        amount,
                        dates[0],
                        dates[1],
                        payment_day,
                        description,
                        use,
                        instalments,
                        due_instalment,
                    )

                    logger.info(f"Your new Debit '{name}' is saved!")
                    return

        logger.error(f"{validator} is not valid")
    except Exception as e:
        logger.error(f"{e}")
