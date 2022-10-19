from src.bussines.nubank import Nubank_API
from src.helpers.clear import clean_output
from loguru import logger


@clean_output
def update_nubank_statment():
    try:
        Nubank_API().update_statment()
    except Exception as error:
        logger.error(error)
