from loguru import logger
from src.bussines.atm import Statment_ATM
from src.helpers.validators import ATMValidatorException
from src.helpers.clear import clean_output


@clean_output
def update_establishment(establishment=None, details=None, geolocation=None, retries=0):
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
def get_establishment(name):
    try:
        if establishment_info := Statment_ATM().get_establishment_info(name):
            logger.info(f"Nome: {establishment_info['name']}")
            logger.info(
                f"Data de Criação do registro: {establishment_info['created_at']}"
            )
            if establishment_info["details"]:
                logger.info(f"Detalhes: {establishment_info['details']}")
            if establishment_info["address"]:
                logger.info(f"Endereço: {establishment_info['address']}")
            if establishment_info["is_pf"]:
                logger.info(f"Pessoa física: {establishment_info['is_pf']}")
        else:
            logger.error("Establishment not found...")
    except Exception as error:
        logger.error(error)


@clean_output
def get_establishment_spend(name, period):
    try:
        if value := Statment_ATM().get_establishment_statment(
            name, period
        ):
            logger.info(f"{name.title()} entre {period} até hoje...")
            logger.info(f"Balanço: R$ {value:.2f}")
        else:
            logger.error(f"Establishment not found for {period}...")
        pass
    except Exception as error:
        logger.error(error)
