from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from pydantic_sqlalchemy import sqlalchemy_to_pydantic

from . import Base


class Variant(Base):
    __tablename__ = "variants"

    chromosome = Column(String, primary_key=True)
    position = Column(String, primary_key=True)
    rsid = Column(String, unique=True)
    ref = Column(String)
    alt = Column(String)
    info = Column(String)


PydanticVariant = sqlalchemy_to_pydantic(Variant)
