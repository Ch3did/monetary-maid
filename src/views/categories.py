import arrow
from loguru import logger
from tabulate import tabulate

from src.bussines.categories import Category_ATM
from src.helpers.clear import clean_output
from src.helpers.validators import is_amount_valid


@clean_output
def create_category_view():
    try:
        print("----------Create New Category ")
        name = input("Name: ")
        description = input("Description: ")
        if expected := is_amount_valid(input("Expected (%.2): ")):
            Category_ATM().add_category(name.lower(), description, expected)
            print(f"Category {name.title()} created sucessfully")
        else:
            print("Expected is not valid")
    except Exception as error:
        logger.error(f"{error}")


@clean_output
def get_categories_info_view(name):
    try:
        data = Category_ATM().get_categories_list(name)
        table = [
            (
                "Name",
                "Expected",
                "Description",
                "Is an Spend",
            )
        ]

        for item in data:
            lista = (
                item.name,
                item.expected,
                item.description,
                item.is_spend,
            )
            table.append(lista)

        print(tabulate(table, headers="firstrow"))

    except Exception as error:
        logger.error(f"{error}")
