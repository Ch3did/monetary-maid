from loguru import logger

from src.bussines.config import make_migrate
from src.models.atm import bank_raiser


def migrate():
    if bank_raiser():
        make_migrate()
        logger.info("Banks already up")
