import arrow
from loguru import logger
from tabulate import tabulate

from src.bussines.categories import Category_ATM
from src.helpers.clear import clean_output


@clean_output
def create_category_view():
    try:
        print("----------Create New Category")
        print("------------------------------\n")
        name = input("Name: ")
        description = input("Description: ")
        expected = float(input("Expected (%.2): "))
        Category_ATM().add_category(name.lower(), description, expected)
        print(f"Category {name.title()} created sucessfully")
    except Exception as error:
        logger.error(f"{error}")


@clean_output
def get_categories_info_view(search_type):

    try:
        data = Category_ATM().get_categories_list(search_type)
        if data:

            table = [
                (
                    "ID",
                    "Name",
                    "Expected",
                    "Description",
                    "Created at",
                )
            ]
            for item in data:
                lista = (
                    item.id,
                    item.name,
                    item.expected,
                    item.description,
                    item.created_at,
                )
                table.append(lista)

            print(tabulate(table, headers="firstrow"))
        else:
            print(f"Category {search_type} Not Found")

    except Exception as error:
        logger.error(f"{error}")
