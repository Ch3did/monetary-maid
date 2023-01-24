import arrow
from loguru import logger
from tabulate import tabulate

from src.bussines.categories import Category_ATM
from src.bussines.debit import Debit_ATM
from src.bussines.nubank import Nubank_API
from src.helpers.clear import clean_output


@clean_output
def update_bank_statment_view():
    print("------------------Update Statment")
    print("---------------------------------\n")
    try:
        Nubank_API().update()
    except Exception as error:
        logger.error(error)


@clean_output
def list_debit_from_period_view(period):
    print("--------------------------Get debit list ")
    print("----------------------------------------\n")
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
    print("----------Update Category from Debit ")
    print("-------------------------------------\n")
    try:
        data = Category_ATM().get_categories_list(0)
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


@clean_output
def get_debit_by_id_view(id):
    print("--------------------------Get  Debit ")
    print("-------------------------------------\n")
    try:

        if debit := Debit_ATM().get_debit(id):
            category = Category_ATM().get_category_by_id(debit.category)
            print()
            debit_list = [
                (
                    "Local",
                    "Data",
                    "Tipo de Transação",
                    "Valor",
                    "Description",
                    "Category",
                ),
                (
                    debit.establishment,
                    arrow.get(debit.date).format("YY-MM-DD"),
                    debit.typename,
                    debit.amount,
                    debit.description,
                    category[0].name,
                ),
            ]

            print("\n", tabulate(debit_list, headers="firstrow"), "\n")

    except Exception as error:
        print(error)
