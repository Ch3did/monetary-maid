import arrow
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from ..helpers.database import Database

Base = declarative_base()


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    expected = Column(Numeric, nullable=True)
    liquid = Column(Numeric)
    created_at = Column(
        String(7), default=arrow.now().strftime("%m-%Y")
    )  # Data que foi adicionado
    upated_at = Column(
        String(7), default=arrow.now().strftime("%m-%Y")
    )  # Data que foi alterado
    is_visible = Column(Boolean, default=True)
    statment = relationship("Statment")


class Statment(Base):
    __tablename__ = "statments"
    id = Column(Integer, primary_key=True)
    checknum = Column(String(100), nullable=False)
    detail = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    typename = Column(String(100), nullable=False)
    amount = Column(Numeric, nullable=False)
    # ForeignKey
    statment_type_id = Column(Integer, ForeignKey("statment_types.id"))
    categories_id = Column(Integer, ForeignKey("categories.id"))
    establishment_id = Column(Integer, ForeignKey("establishments.id"))


class Establishments(Base):
    __tablename__ = "establishments"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    created_at = Column(
        String(7), default=arrow.now().strftime("%m-%Y")
    )  # Data que foi adicionado
    upated_at = Column(
        String(7), default=arrow.now().strftime("%m-%Y")
    )  # Data que foi alterado
    detail = Column(Text, nullable=True)
    address = Column(String(60), nullable=True)
    statment = relationship("Statment")
    is_visible = Column(Boolean, default=True)
    is_pf = Column(Boolean, default=False)

    # TODO: added Typo de estabelecimento


class StatmentTypes(Base):
    __tablename__ = "statment_types"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    is_math_use = Column(Boolean, default=False)
    is_negative = Column(Boolean)
    statment = relationship("Statment")


def bank_raiser():
    try:
        engine = Database().engine
        Base.metadata.create_all(engine)
        return True
    except Exception as error:
        return False
