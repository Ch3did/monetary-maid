from loguru import logger

from src.bussines.config import Config
from src.helpers.clear import clean_output
from src.models.atm import bank_raiser


@clean_output
def run_migrate_view():
    if bank_raiser():
        Config().make_migrate()
        logger.info("Banks already up")
