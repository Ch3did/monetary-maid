from loguru import logger

from src.bussines.atm import Statment_ATM
from src.helpers.clear import clean_output
from src.helpers.validators import ATMValidatorException


@clean_output
def update_establishment_view(
    establishment=None, details=None, geolocation=None, retries=0
):
    try:
        if not establishment:
            establishment = input("Establishment: ")
        if not details:
            details = input("Details: ")
            geolocation = input("Geolocation: ")

        Statment_ATM().update_establishment_datails(establishment, details, geolocation)

        logger.info(f"Updated {establishment} info!")

    except ATMValidatorException as error:
        if error.message == "Unknow Establishment":
            logger.error(f"{error.message}... Please, try again...")
            if error.can_retry:
                retries += 1
                update_establishment(
                    details=error.details,
                    geolocation=error.geolocation,
                    retries=retries,
                )

    except Exception as error:
        logger.error(error)


@clean_output
def get_establishment_info_view(name):
    try:
        if establishment_info := Statment_ATM().get_establishment_info(name):
            for item in establishment_info:
                print(f"Name: {item['name'].title()}  |   ID: {item['id']}")
                print(f"Original name: {item['original_name'].title()}")
                print(f"Created in: {item['created_at']}")
                if item["details"]:
                    print(f"Details: {item['details']}")
                if item["address"]:
                    print(f"Address: {item['address']}")
                if item["is_pf"]:
                    print(f"Pf: {item['is_pf']}")

                if item["country"]:
                    print(f"Country: {item['country']}")
                print(
                    "_____________________________________________________________________________________"
                )

        else:
            logger.error("Establishment not found...")
    except Exception as error:
        logger.error(error)


@clean_output
def get_establishment_spend_view(name, period):
    try:
        if value := Statment_ATM().get_establishment_statment(name, period):
            logger.info(f"{name.title()} from {period} to today...")
            logger.info(f"Balanço: R$ {value:.2f}")
        else:
            logger.error(f"Establishment not found for {period}...")
        pass
    except Exception as error:
        logger.error(error)


# TODO: o plot tem que estar aki na view
@clean_output
def plot_period_by_establishment_view(name):
    try:
        dicionario_de_totais = Statment_ATM().get_establishment_per_month(name)
    except Exception as error:
        logger.error(error)
