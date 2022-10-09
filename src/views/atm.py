from loguru import logger

from src.bussines.atm import Statment_ATM
from src.bussines.nubank import Nubank_API
from src.helpers.validators import ATMValidatorException
from src.views.atm import *


def update_establishment(establishment=None, details=None, geolocation=None, retries=0):
    try:
        if not establishment:
            establishment = input("Establishment: ")
        if not details:
            details = input("Details: ")
            geolocation = input("Geolocation: ")

        Statment_ATM().update_establishment(establishment, details, geolocation)

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


def get_establishment(name=None, period=None):
    try:
        atm = Statment_ATM()
        if period:
            atm.get_stb_statment(name, period)
        else:
            atm.get_stb_info(name)
    except Exception as error:
        logger.error(error)


def update_nubank_statment():
    try:
        Nubank_API().update_statment()
    except Exception as error:
        logger.error(error)
