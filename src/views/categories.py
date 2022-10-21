from loguru import logger

from src.bussines.atm import Statment_ATM
from src.helpers.clear import clean_output
from src.helpers.validators import ATMValidatorException, is_amount_valid


@clean_output
def create_category_view():
    try:
        print("----------Create New Category ")
        name = input("Name: ")
        description = input("Description: ")
        if expected := is_amount_valid(input("Expected (%.2): ")):
            Statment_ATM().add_category(name.lower(), description, expected)
            print(f"Category {name.title()} created sucessfully")
            return
        logger.error("Expected is not valid")
    except Exception as e:
        logger.error(f"{e}")
