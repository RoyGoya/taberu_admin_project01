# coding: utf-8
from sqlalchemy import Boolean, CHAR, Column, DateTime, Float, ForeignKeyConstraint, Index, Integer, String
from sqlalchemy.orm import relationship

from ..database import Base


class Factor(Base):
    __tablename__ = 'factor'

    pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    pattern2 = Column(CHAR(1), primary_key=True, nullable=False)
    pattern3 = Column(CHAR(2), primary_key=True, nullable=False)
    pattern4 = Column(CHAR(2), primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    eng_name = Column(String(100), nullable=False)
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))
    has_sub = Column(Boolean, nullable=False)


class FactorSet(Base):
    __tablename__ = 'factor_set'
    __table_args__ = (
        ForeignKeyConstraint(['factor_pattern1', 'factor_pattern2', 'factor_pattern3', 'factor_pattern4'], ['factor.pattern1', 'factor.pattern2', 'factor.pattern3', 'factor.pattern4']),
        ForeignKeyConstraint(['nutrient_dt_pattern', 'nutrient_pattern1', 'nutrient_pattern2', 'nutrient_serial'], ['nutrient.dt_pattern', 'nutrient.pattern1', 'nutrient.pattern2', 'nutrient.serial']),
        ForeignKeyConstraint(['unit_pattern1', 'unit_pattern2'], ['unit_common.pattern1', 'unit_common.pattern2']),
        Index('idx_fs_unit', 'unit_pattern1', 'unit_pattern2'),
        Index('idx_fs_factor', 'factor_pattern1', 'factor_pattern2', 'factor_pattern3', 'factor_pattern4'),
        Index('idx_fs_nutrient', 'nutrient_dt_pattern', 'nutrient_pattern1', 'nutrient_pattern2', 'nutrient_serial')
    )

    nutrient_dt_pattern = Column(CHAR(1), primary_key=True, nullable=False)
    nutrient_pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    nutrient_pattern2 = Column(CHAR(2), primary_key=True, nullable=False)
    nutrient_serial = Column(Integer, primary_key=True, nullable=False)
    is_active = Column(Boolean, nullable=False)
    factor_pattern1 = Column(CHAR(1), primary_key=True, nullable=False)
    factor_pattern2 = Column(CHAR(1), primary_key=True, nullable=False)
    factor_pattern3 = Column(CHAR(2), primary_key=True, nullable=False)
    factor_pattern4 = Column(CHAR(2), primary_key=True, nullable=False)
    quantity = Column(Float, nullable=False)
    unit_pattern1 = Column(CHAR(2), nullable=False)
    unit_pattern2 = Column(CHAR(2), nullable=False)

    factor = relationship('Factor')
    nutrient = relationship('Nutrient')
    unit_common = relationship('UnitCommon')
