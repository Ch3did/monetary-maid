import arrow
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    MetaData,
    Numeric,
    String,
    Text,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from src.get_env import SCHEMA

from ..helpers.database import Database

metadata_obj = MetaData(schema=SCHEMA)

Base = declarative_base(metadata=metadata_obj)


class Bills(Base):
    __tablename__ = "bills"

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
    categories_id = Column(Integer, ForeignKey("categories.id"))


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    expected = Column(Numeric, nullable=True)
    liquid = Column(Numeric)
    created_at = Column(
        DateTime, default=arrow.now().strftime("%Y-%m-%d")
    )  # Data da primeira vez que foi usado
    updated_at = Column(
        DateTime, default=arrow.now().strftime("%Y-%m-%d")
    )  # Data que foi alterado
    is_visible = Column(Boolean, default=True)
    # TODO: Add key-words
    statment = relationship("Statment")
    bills = relationship("Bills")


class Statment(Base):
    __tablename__ = "debit"
    id = Column(Integer, primary_key=True)
    checknum = Column(String(100), nullable=False)
    detail = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    typename = Column(String(100), nullable=False)
    amount = Column(Numeric, nullable=False)
    # ForeignKey
    statment_type_id = Column(Integer, ForeignKey("types.id"))
    categories_id = Column(Integer, ForeignKey("categories.id"))
    establishment_id = Column(Integer, ForeignKey("establishments.id"))


class Credit_Statement(Base):
    __tablename__ = "credit"
    id = Column(Integer, primary_key=True)
    checknum = Column(String(100), nullable=False)  #   #sem detalhes
    category = Column(String(60), nullable=False)  #  # sem detalhes
    total_amount = Column(Numeric, nullable=False)  #  # amoutn sem detalhes
    instalment_amount = Column(Numeric, nullable=False)  # (amount *100) # detalhe
    status = Column(String(60), nullable=False)  # (status) # detalhe
    instalment_date = Column(DateTime)  # (post_date) # detalhe
    instalment_index = Column(Integer)  # (index) # detalhe
    instalment_promotion_reason = Column(
        String(60), nullable=True
    )  # (promotion_reason) # detalhe
    purchase_date = Column(DateTime)  #  #Quando foi criado sem detalhes
    title = Column(String(60), nullable=False)  #  # sem detalhes
    source = Column(String(60), nullable=False)  #  #sem detalhes
    card_last_digits = Column(Integer)
    card_type = Column(String(40), nullable=False)
    amount_without_iof = Column(Numeric, nullable=False)
    card_id = Column(String(60), nullable=False)
    event_type = Column(String(60), nullable=False)
    establishment_id = Column(Integer, ForeignKey("establishments.id"))


class Establishments(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    original_name = Column(String(100), nullable=False)
    created_at = Column(
        DateTime, default=arrow.now().strftime("%Y-%m-%d")
    )  # Data da primeira vez que foi usado
    updated_at = Column(
        DateTime, default=arrow.now().strftime("%Y-%m-%d")
    )  # Data que foi alterado
    detail = Column(Text, nullable=True, default=None)
    address = Column(String(60), nullable=True, default=None)
    is_visible = Column(Boolean, default=True)
    is_pf = Column(Boolean, default=False)
    mcc = Column(Integer, nullable=True, default=None)  # Merchant Category Code
    country = Column(String(60), nullable=True)

    statment = relationship("Statment")
    credit_statment = relationship("Credit_Statement")

    # TODO: added Typo de estabelecimento


class StatmentTypes(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    is_math_use = Column(Boolean, default=False)
    is_negative = Column(Boolean)
    statment = relationship("Statment")


def bank_raiser():
    engine = Database().engine
    Base.metadata.create_all(engine)
