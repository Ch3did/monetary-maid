from loguru import logger

from src.helpers.database import Database
from src.helpers.validators import ATMValidatorException
from src.models.atm import Establishments, Statment, StatmentTypes

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
        if values := (
            self.conn.query(Establishments.id)
            .filter(Establishments.name == establishment)
            .all()
        ):
            return int(values[0][0])

        self.conn.add(Establishments(name=establishment))
        logger.info(f"Finded new establishment: {establishment}")
        self.conn.commit()
        self.conn.close()
        return self.add_establishment(establishment)

    def add_type(self, type):
        if values := (
            self.conn.query(StatmentTypes.id).filter(StatmentTypes.name == type).all()
        ):
            return int(values[0][0])

        title_type = StatmentTypes(name=type)

        negative = (
            "compra",
            "pagamento",
            "reserva de ipo",
            "saque",
            "transferência enviada",
        )
        positive = (
            "planejamento concluído",
            "devolvido",
            "reembolso",
            "recebido",
            "estorno",
            "transferência recebida",
        )

        if [
            negative_sentence
            for negative_sentence in negative
            if negative_sentence in type.lower()
        ]:
            title_type.is_negative = True
            title_type.is_math_use = True
        elif [
            positive_sentence
            for positive_sentence in positive
            if positive_sentence in type.lower()
        ]:
            title_type.is_negative = False
            title_type.is_math_use = True
        else:
            title_type.is_math_use = False

        self.conn.add(title_type)
        logger.info(f"Novo tipo {type} inserido no banco")
        self.conn.commit()
        self.conn.close()

        return self.add_type(type)

    def add_statment(self, item):
        # Valida registro de transação no banco
        if not (
            self.conn.query(Statment)
            .filter(Statment.checknum == item["checknum"])
            .filter(Statment.statment_type_id == item["type_id"])
            .filter(Statment.detail == item["detail"])
            .filter(Statment.date == item["date"])
            .filter(Statment.typename == item["typename"])
            .filter(Statment.amount == item["amount"])
            .all()
        ):
            transaction = Statment(
                checknum=item["checknum"],
                detail=item["detail"],
                date=item["date"],
                typename=item["typename"],
                amount=item["amount"],
                statment_type_id=item["type_id"],
                establishment_id=item["establishment_id"],
            )
            self.conn.add(transaction)
            logger.info(f"inserido no banco: {item['title']}")
            self.conn.commit()
            self.conn.close()
