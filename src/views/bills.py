from loguru import logger

from src.bussines.atm import Statment_ATM
from src.helpers.clear import clean_output
from src.helpers.validators import is_amount_valid, is_date_valid, is_payment_day_valid


@clean_output
def create_bill_view():
    try:
        print("----------Create New Bill ")
        name = input("Name: ")
        description = input("Description: ")
        if expected := is_amount_valid(input("Expected (%.2): ")):
            Statment_ATM().add_category(name.lower(), description, expected)
            print(f"Category {name.title()} created sucessfully")
            return
        logger.error("Expected is not valid")
    except Exception as e:
        logger.error(f"{e}")

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

                    Statment_ATM().add_bill(
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
