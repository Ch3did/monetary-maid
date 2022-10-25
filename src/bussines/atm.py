import arrow
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt

from src.helpers.database import Database
from src.helpers.validators import ATMValidatorException
from src.models.atm import Bills, Categories, Establishments, Statment, StatmentTypes

# TODO: Criar lógica para pegar geolocalização dos estabelecimentos


class Statment_ATM:
    def __init__(self):

        self.conn = Database().session()

    # Put

    def _add_establishment(self, name, date):
        if establishment := (
            self.conn.query(Establishments)
            .filter(Establishments.name == name.lower().rstrip())
            .first()
        ):
            if arrow.get(establishment.created_at) > arrow.get(date):
                establishment.created_at = date
                self.conn.commit()
            return int(establishment.id)

        self.conn.add(Establishments(name=name.lower().rstrip(), created_at=date))
        logger.info(f"Finded new establishment: {name.title()}")
        self.conn.commit()
        self.conn.close()
        return self._add_establishment(name, date)

    def _add_type(self, type):
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

        return self._add_type(type)

    def _add_statment(self, item):
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

    def add_category(self, name, description, expected):
        # TODO: View precisa mandar o dado tratado
        if (
            self.conn.query(Categories.id)
            .filter(Categories.name == name.rstrip())
            .first()
        ):
            raise ATMValidatorException(
                message="Category already exists... ",
                description=description,
                expected=expected,
            )

        category = Categories(
            name=name, description=description, expected=expected, is_visible=True
        )

        self.conn.add(category)
        self.conn.commit()
        self.conn.close()

    def add_bill(
        self,
        name,
        amount,
        dates,
        payment_day,
        description,
        use,
        instalments=None,
        due_instalment=None,
    ):
        if self.conn.query(Bills.id).filter(Bills.name == name.rstrip()).first():
            # TODO: criar nova exception para cada tabela
            raise ATMValidatorException(
                message="Bill already exists... ",
                description=description,
                # expected=expected,
                # amount, dates, payment_day, description, use, instalments=None, due_instalment=None
            )

        bill = Bills(
            name=name,
            amount=amount,
            dates=dates,
            payment_day=payment_day,
            description=description,
            use=use,
            instalments=instalments,
            due_instalment=due_instalment,
        )

        self.conn.add(bill)
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
                    if (
                        self.conn.query(StatmentTypes.is_negative)
                        .filter(StatmentTypes.id == transaction_type_id)
                        .first()
                    )[0]:
                        value -= float(item[0])
                    else:
                        value += float(item[0])

                return value
        else:
            raise ATMValidatorException(
                message="Unknow Establishment",
                establishment=establishment_name,
            )

    # Plot

    # retornar um dicionário com totais de um estabelecimento separados por mês
    def get_establishment_per_month(self, establishment_name):
        if establishment := (
            self.conn.query(Establishments)
            .filter(Establishments.name == establishment_name.lower())
            .first()
        ):
            all_statment_data = (
                self.conn.query(
                    Statment.date, Statment.amount, Statment.statment_type_id
                )
                .filter(Statment.establishment_id == establishment.id)
                .all()
            )
            pandas_dict = {"amount": [], "date": []}
            for item in all_statment_data:
                is_negative, is_math_use = (
                    self.conn.query(
                        StatmentTypes.is_negative, StatmentTypes.is_math_use
                    )
                    .filter(StatmentTypes.id == item.statment_type_id)
                    .first()
                )
                if is_math_use:
                    pandas_dict["amount"].append(
                        item.amount * -1 if is_negative else item.amount
                    )
                    pandas_dict["date"].append(item.date)
            new = pd.DataFrame.from_dict(pandas_dict)
            new = new.groupby("date")
            new.count().plot()
            plt.show()
