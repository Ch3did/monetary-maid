from loguru import logger

from src.helpers.database import Database
from src.helpers.validators import ATMValidatorException
from src.models.atm import Establishments, Statment, StatmentTypes


# TODO: Criar lógica para pegar geolocalização dos estabelecimentos


class Statment_ATM:
    def __init__(self):

        self.conn = Database().session()

    # Put
    def update_establishment_datails(self, establishment, details, geolocation):
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
            .filter(Establishments.name == establishment.lower())
            .all()
        ):
            return int(values[0][0])

        self.conn.add(Establishments(name=establishment.lower()))
        logger.info(f"Finded new establishment: {establishment.title()}")
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
            is_negative = True
            is_math_use = True
        elif [
            positive_sentence
            for positive_sentence in positive
            if positive_sentence in type.lower()
        ]:
            is_negative = False
            is_math_use = True
        else:
            is_negative = None
            is_math_use = False

        title_type = StatmentTypes(
            name=type, is_math_use=is_math_use, is_negative=is_negative
        )

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

    # Get
    def get_establishment_info(self, establishment_name):
        if data := (
            self.conn.query(Establishments)
            .filter(Establishments.name == establishment_name.lower())
            .first()
        ):
            return {
                "name": data.name,
                "created_at": data.created_at,
                "details": data.detail,
                "address": data.address,
                "is_pf": data.is_pf,
            }

        return None

    def get_establishment_statment(self, establishment_name, period):
        value = 0
        if id := (
            self.conn.query(Establishments.id)
            .filter(Establishments.name == establishment_name.lower())
            .first()
        ):
            if data := (
                self.conn.query(Statment.amount, Statment.statment_type_id)
                .filter(Statment.establishment_id == id[0])
                .filter(Statment.date >= period)
                .all()
            ):

                for item in data:
                    transaction_type_id = item[1]
                    if (self.conn.query(StatmentTypes.is_negative).filter(StatmentTypes.id == transaction_type_id).first())[0]:
                        value -= float(item[0])
                    else:
                        value += float(item[0])

                return value
        return None
