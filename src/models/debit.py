import arrow
from sqlalchemy import Column, DateTime, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.sql.sqltypes import Boolean

from src.models.base import Base


class Debit(Base):
    __tablename__ = "debit"
    id = Column(Integer, primary_key=True)
    checknum = Column(String(100), nullable=False)
    detail = Column(Text, nullable=False)
    date = Column(DateTime, nullable=False)
    typename = Column(String(100), nullable=False)
    amount = Column(Numeric, nullable=False)
    establishment = Column(String(100), nullable=True)
    is_negative = Column(Boolean)
    description = Column(Text, nullable=True)
    # ForeignKey
    category = Column(Integer, ForeignKey("categories.id"))
