from loguru import logger

from monetary_maid.helpers.database import Database
from monetary_maid.helpers.validators import ATMValidatorException
from monetary_maid.model import ATM, Establishments

# TODO: criar methodo para atualizar os dados de estabelecimento


# TODO: Criar lógica para pegar geolocalização dos estabelecimentos


class ATM_API:
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
            self.conn.query(ATM)
            .filter(ATM.checknum == item["checknum"])
            .filter(ATM.title == item["title"])
            .filter(ATM.detail == item["detail"])
            .filter(ATM.date == item["date"])
            .filter(ATM.typename == item["typename"])
            .filter(ATM.amount == item["amount"])
            .all()
        ):
            transaction = ATM(
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
