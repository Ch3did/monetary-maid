import arrow
from loguru import logger
from tabulate import tabulate

from src.bussines.categories import Category_ATM
from src.helpers.clear import clean_output


@clean_output
def create_category_view():
    try:
        print("----------Create New Category ")
        name = input("Name: ")
        description = input("Description: ")
        expected = float(input("Expected (%.2): "))
        Category_ATM().add_category(name.lower(), description, expected)
        print(f"Category {name.title()} created sucessfully")
    except Exception as error:
        logger.error(f"{error}")


@clean_output
def get_categories_info_view(name):
    try:
        data = Category_ATM().get_categories_list(name)
        table = [
            (
                "ID",
                "Name",
                "Expected",
                "Description",
                "Is an Spend",
            )
        ]

        for item in data:
            lista = (
                item.id,
                item.name,
                item.expected,
                item.description,
                item.is_spend,
            )
            table.append(lista)

        print(tabulate(table, headers="firstrow"))

    except Exception as error:
        logger.error(f"{error}")
