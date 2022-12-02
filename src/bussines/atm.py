import arrow
import pandas as pd
from loguru import logger
from matplotlib import pyplot as plt

from src.helpers.database import Database
from src.helpers.validators import ATMValidatorException
from src.models.atm import (
    Bills,
    Categories,
    Credit_Statement,
    Establishments,
    Statment,
    StatmentTypes,
)

# TODO: Criar lógica para pegar geolocalização dos estabelecimentos


class Statment_ATM:
    def __init__(self):

        self.conn = Database().session()

    # Put

    def _add_establishment(self, data):
        if establishment := (
            self.conn.query(Establishments)
            .filter(Establishments.name == data["name"])
            .filter(Establishments.mcc == data.get("mcc"))
            .filter(Establishments.country == data["country"])
            .first()
        ):

            if arrow.get(establishment.created_at) > arrow.get(data["date"]):
                establishment.created_at = data["date"]

            elif arrow.get(establishment.updated_at) < arrow.get(data["date"]):
                establishment.updated_at = data["date"]

            self.conn.commit()
            return int(establishment.id)

        data["detail"] = data.get("detail", None)
        data["address"] = data.get("address", None)
        data["is_visible"] = data.get("is_visible", True)
        data["is_pf"] = data.get("is_pf", False)
        data["mcc"] = data.get("mcc", None)

        establishment = Establishments(
            name=data["name"].lower().rstrip().strip("-").strip("\n").rstrip().lstrip(),
            original_name=data["sanatize_original_name"],
            detail=data["detail"],
            address=data["address"],
            is_visible=data["is_visible"],
            is_pf=data["is_pf"],
            mcc=data["mcc"],
            country=data["country"],
        )

        self.conn.add(establishment)
        logger.info(f"Finded new establishment: {data['name'].title()}")
        self.conn.commit()
        self.conn.close()
        return self._add_establishment(data)

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
        logger.info(f"Novo tipo `{type}` inserido no banco")
        self.conn.commit()
        self.conn.close()

        return self._add_type(type)

    # TODO: Quando for fazer o update, verificar se há alguma bill com mesmo valor e lincada ao mesmo establishment
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

    def _add_credit_statment(self, item):
        if not (
            self.conn.query(Credit_Statement)
            .filter(Credit_Statement.checknum == item["checknum"])
            .filter(Credit_Statement.category == item["category"])
            .filter(Credit_Statement.total_amount == item["total_amount"])
            .filter(Credit_Statement.instalment_amount == item["instalment_amount"])
            .filter(Credit_Statement.status == item["status"])
            .filter(Credit_Statement.instalment_date == item["instalment_date"])
            .filter(Credit_Statement.instalment_index == item["instalment_index"])
            .filter(
                Credit_Statement.instalment_promotion_reason
                == item["instalment_promotion_reason"]
            )
            .filter(Credit_Statement.purchase_date == item["purchase_date"])
            .filter(Credit_Statement.title == item["title"])
            .filter(Credit_Statement.source == item["source"])
            .filter(Credit_Statement.card_last_digits == item["card_last_digits"])
            .filter(Credit_Statement.card_type == item["card_type"])
            .filter(Credit_Statement.amount_without_iof == item["amount_without_iof"])
            .filter(Credit_Statement.card_id == item["card_id"])
            .filter(Credit_Statement.event_type == item["event_type"])
            .filter(Credit_Statement.establishment_id == item["establishment_id"])
            .all()
        ):
            transaction = Credit_Statement(
                checknum=item["checknum"],
                category=item["category"],
                total_amount=item["total_amount"],
                instalment_amount=item["instalment_amount"],
                status=item["status"],
                instalment_date=item["instalment_date"],
                instalment_index=item["instalment_index"],
                instalment_promotion_reason=item["instalment_promotion_reason"],
                purchase_date=item["purchase_date"],
                title=item["title"],
                source=item["source"],
                card_last_digits=item["card_last_digits"],
                card_type=item["card_type"],
                amount_without_iof=item["amount_without_iof"],
                card_id=item["card_id"],
                event_type=item["event_type"],
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
