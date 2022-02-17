import arrow
from sqlalchemy import Column, DateTime, Integer, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import Boolean
from sqlalchemy.types import JSON

from bussines.helpers.database import Database

Base = declarative_base()


class FixedDebits(Base):
    __tablename__ = "fixed_debits"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    amount = Column(Numeric, nullable=False)
    start_date = Column(DateTime, nullable=False, default=arrow.now())
    end_date = Column(DateTime, nullable=True)
    payment_day = Column(String(2), nullable=True, default="01")
    description = Column(Text, nullable=False)
    use = Column(Boolean, nullable=False, default=True)


class FloatedDebits(Base):
    __tablename__ = "floated_debits"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    amount = Column(Numeric, nullable=False)
    instalments = Column(Integer, nullable=False, default=1)
    due_instalment = Column(Numeric, nullable=False)
    start_date = Column(DateTime, nullable=False, default=arrow.now())
    end_date = Column(DateTime, nullable=True)
    payment_day = Column(String(2), nullable=True, default="01")
    description = Column(Text, nullable=False)
    use = Column(Boolean, nullable=False, default=True)


class Wallet(Base):
    __tablename__ = "wallet"

    id = Column(Integer, primary_key=True)
    gross = Column(Numeric)
    fixed_debits = Column(Numeric)
    floated_debits = Column(Numeric)
    net = Column(Numeric)
    invest = Column(Numeric)
    big_save = Column(Numeric)
    month_emergency = Column(Numeric)
    available = Column(Numeric)
    timestamp = Column(DateTime, default=arrow.now())
    date = Column(String(7), default=arrow.now().strftime("%m-%Y"))
    debits_details = Column(JSON)


if __name__ == "__main__":
    engine = Database().engine
    Base.metadata.create_all(engine)
