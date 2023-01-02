import arrow
from loguru import logger
from tabulate import tabulate

from src.bussines.categories import Category_ATM
from src.bussines.debit import Debit_ATM
from src.bussines.nubank import Nubank_API
from src.helpers.clear import clean_output


@clean_output
def update_nubank_statment_view():
    try:
        Nubank_API().update()
    except Exception as error:
        logger.error(error)


@clean_output
def list_debit_from_period_view(period):
    try:
        debit_list = [
            (
                "id",
                "establishment",
                "date",
                "typename",
                "amount",
                "description",
                "category",
            )
        ]
        data = Debit_ATM().get_debits(period)
        for item in data:
            values = (
                item[0].id,
                item[0].establishment,
                arrow.get(item[0].date).format("YYYY-MM-DD"),
                item[0].typename,
                f"{item[0].amount:,.2f}",
                item[0].description,
                item[1].name,
            )
            debit_list.append(values)

        print(tabulate(debit_list, headers="firstrow"))

    except Exception as error:
        logger.error(f"{error}")


@clean_output
def update_debit_category_view(id):
    try:
        print("----------Update Category from Debit ")
        data = Category_ATM().get_categories_list("all")
        table = [("ID", "Name")]

        for item in data:
            lista = (item.id, item.name)
            table.append(lista)

        print(tabulate(table, headers="firstrow"))

        category_id = int(input(f"\nInput category_id for debit {id}?: "))

        Debit_ATM().update_debits_category(id, category_id)

        print("Changed sucessfully!")
    except Exception as error:
        logger.error(f"{error}")
