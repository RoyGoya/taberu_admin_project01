# coding: utf-8
from sqlalchemy import Boolean, CHAR, Column, DateTime, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base
from ..helpers.timezone_gen import get_utc_datetime


class DataPattern(Base):
    __tablename__ = 'data_pattern'

    pattern = Column(CHAR(1), primary_key=True)
    name = Column(String(100), nullable=False)
    is_active = Column(Boolean, nullable=False)


class Nutrient(Base):
    __tablename__ = 'nutrient'

    dt_pattern = Column(CHAR(1), primary_key=True, nullable=False)
    pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    serial = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    has_sub = Column(Boolean, nullable=False)
    created_datetime = Column(DateTime(True), nullable=False, default=get_utc_datetime)
    modified_datetime = Column(DateTime(True), nullable=False, default=get_utc_datetime)
    eng_name = Column(String(100), nullable=False)
    eng_plural = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))


class NutrientPattern(Base):
    __tablename__ = 'nutrient_pattern'

    pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    eng_name = Column(String(100), nullable=False)
    eng_plural = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))


class NutrientSet(Base):
    __tablename__ = 'nutrient_set'
    __table_args__ = (
        ForeignKeyConstraint(['sub_dt_pattern', 'sub_pattern1', 'sub_pattern2', 'sub_serial'], ['nutrient.dt_pattern', 'nutrient.pattern1', 'nutrient.pattern2', 'nutrient.serial']),
        ForeignKeyConstraint(['super_dt_pattern', 'super_pattern1', 'super_pattern2', 'super_serial'], ['nutrient.dt_pattern', 'nutrient.pattern1', 'nutrient.pattern2', 'nutrient.serial']),
        Index('idx_nutrient_set_sub_dt_pattern', 'sub_dt_pattern', 'sub_pattern1', 'sub_pattern2', 'sub_serial'),
        Index('idx_nutrient_set_super_dt_pattern', 'super_dt_pattern', 'super_pattern1', 'super_pattern2', 'super_serial')
    )

    super_dt_pattern = Column(CHAR(1), primary_key=True, nullable=False)
    super_pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    super_pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    super_serial = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    sub_dt_pattern = Column(CHAR(1), primary_key=True, nullable=False)
    sub_pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    sub_pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    sub_serial = Column(Integer, primary_key=True, nullable=False)

    nutrient = relationship('Nutrient', primaryjoin='NutrientSet.sub_dt_pattern == Nutrient.dt_pattern')
    nutrient1 = relationship('Nutrient', primaryjoin='NutrientSet.super_dt_pattern == Nutrient.dt_pattern')
