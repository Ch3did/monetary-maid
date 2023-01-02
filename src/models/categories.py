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
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import Boolean

from src.models.base import Base


class Categories(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(60), nullable=False)
    description = Column(Text, nullable=True)
    expected = Column(Numeric, nullable=True)
    created_at = Column(
        DateTime, default=arrow.now().strftime("%Y-%m-%d")
    )  # Data da primeira vez que foi usado
    is_visible = Column(Boolean, default=True)
    is_spend = Column(Boolean, default=False)
    # TODO: Add key-words
    debit = relationship("Debit")
