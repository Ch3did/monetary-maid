import sys

from loguru import logger

from src.bussines.categories import Category_ATM
from src.bussines.debit import Debit_ATM
from src.get_env import USER_NAME
from src.helpers.clear import clean_output


@clean_output
def make_homescreen(search_type):
    try:
        categories = Category_ATM().get_categories_list(search_type)
        transactions = Debit_ATM().get_debits()
        plot_relation = {}
        for values in transactions:
            if values[1].name not in plot_relation:
                plot_relation[values[1].name] = 0
            plot_relation[values[1].name] += values[0].amount
        anwser = str(USER_NAME) if USER_NAME else "Sr"
        print((f"----------Wellcome Back {anwser}"))
        print(
            "-------------------------------------------------------------------------------\n"
        )
        for item in categories:
            if item.is_spend:
                bar_len = 45
                count = abs(plot_relation.get(item.name, 0))
                total = abs(item.expected)
                title = item.name.title()
                if total > count:
                    filled_len = int(round(bar_len * float(count) / float(total)))
                    bar = "#" * filled_len + "-" * (bar_len - filled_len)
                else:
                    bar = "#".ljust(bar_len, "#")

                text_bar = (
                    f"{title.ljust(15)}:  [{bar}] | partials: {total-count:,.2f}\n"
                )
                sys.stdout.write(text_bar)

    except Exception as error:
        logger.error(f"{error}")
