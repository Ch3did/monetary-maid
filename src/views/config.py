from loguru import logger

from src.bussines.config import Config
from src.models.atm import bank_raiser
from src.helpers.clear import clean_output


@clean_output
def migrate():
    if bank_raiser():
        Config().make_migrate()
        logger.info("Banks already up")
