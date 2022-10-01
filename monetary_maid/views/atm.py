from loguru import logger

from monetary_maid.bussines.banks.atm import ATM_API
from monetary_maid.helpers.validators import ATMValidatorException
from monetary_maid.views.atm import *


def update_establishment(establishment=None, details=None, geolocation=None, retries=0):
    try:
        if not establishment:
            establishment = input("Establishment: ")
        if not details:
            details = input("Details: ")
            geolocation = input("Geolocation: ")

        ATM_API().update_establishment(establishment, details, geolocation)

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


def get_stablishment(name=None, period=None):
    atm = ATM_API()
    if period:
        atm.get_stb_statment(name, period)
    else:
        atm.get_stb_info(name)
