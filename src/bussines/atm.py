from loguru import logger

from src.helpers.database import Database
from src.helpers.validators import ATMValidatorException
from src.models.atm import Establishments, Statment

# TODO: criar methodo para atualizar os dados de estabelecimento


# TODO: Criar lógica para pegar geolocalização dos estabelecimentos


class Statment_ATM:
    def __init__(self):
        self.conn = Database().session()

    def update_establishment(self, establishment, details, geolocation):
        if id := (
            self.conn.query(Establishments.id)
            .filter(Establishments.name == establishment)
            .all()
        ):
            self.conn.query(Establishments).filter(
                Establishments.id == id[0][0]
            ).update(
                {
                    Establishments.detail: f"{details}",
                    Establishments.address: f"{geolocation}",
                }
            )
            self.conn.commit()
            self.conn.close()
        else:
            raise ATMValidatorException(
                message="Unknow Establishment",
                establishment=establishment,
                details=details,
                geolocation=geolocation,
            )

    def add_establishment(self, establishment):
        if not (
            self.conn.query(Establishments)
            .filter(Establishments.name == establishment)
            .all()
        ):
            self.conn.add(Establishments(name=establishment))
            logger.info(f"Finded new establishment: {establishment}")
            self.conn.commit()
            self.conn.close()

    def add_statment(self, item):
        # Valida registro de transação no banco
        if not (
            self.conn.query(Statment)
            .filter(Statment.checknum == item["checknum"])
            .filter(Statment.title == item["title"])
            .filter(Statment.detail == item["detail"])
            .filter(Statment.date == item["date"])
            .filter(Statment.typename == item["typename"])
            .filter(Statment.amount == item["amount"])
            .all()
        ):
            transaction = Statment(
                checknum=item["checknum"],
                title=item["title"],
                detail=item["detail"],
                date=item["date"],
                typename=item["typename"],
                amount=item["amount"],
            )
            self.conn.add(transaction)
            logger.info(f"inserido no banco: {item['title']}")
            self.conn.commit()
            self.conn.close()
