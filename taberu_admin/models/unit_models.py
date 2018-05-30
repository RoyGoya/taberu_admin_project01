# coding: utf-8
from sqlalchemy import Boolean, CHAR, Column, Float, String

from ..database import Base


class UnitCommon(Base):
    __tablename__ = 'unit_common'

    pattern1 = Column(CHAR(2), primary_key=True, nullable=False)
    pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    symbol = Column(String(30), nullable=False)
    eng_name = Column(String(100), nullable=False)


class UnitUscs(Base):
    __tablename__ = 'unit_uscs'

    pattern1 = Column(CHAR(2), primary_key=True, nullable=False)
    pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    symbol = Column(String(30), nullable=False)
    eng_name = Column(String(100), nullable=False)
    uscs_to_common = Column(Float)
    common_to_uscs = Column(Float)
    co_pattern = Column(CHAR(2), primary_key=True, nullable=False)
