from loguru import logger

from src.bussines.nubank import Nubank_API
from src.helpers.clear import clean_output


@clean_output
def update_nubank_statment_view():
    try:
        Nubank_API().update_statment()
    except Exception as error:
        logger.error(error)
