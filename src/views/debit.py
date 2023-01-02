import arrow
from loguru import logger
from tabulate import tabulate

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
