from loguru import logger

from src.bussines.config import Config
from src.helpers.clear import clean_output


@clean_output
def run_migrate_view():
    try:
        Config().make_migrate()
        logger.info("Banks already up")

    except Exception as error:
        logger.error(f"Tables are Down... {error}")
