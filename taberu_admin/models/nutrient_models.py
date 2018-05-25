# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

from sqlalchemy import Column, Integer, String, CHAR, Boolean, DATETIME, \
    REAL

from ..database import Base
from ..helpers.timezone_gen import utc_now


class Nutrient(Base):
    __tablename__ = 'nutrient'
    dt_pattern = Column(CHAR(1), primary_key=True)
    pattern1 = Column(CHAR(1), primary_key=True)
    pattern2 = Column(CHAR(2), primary_key=True)
    serial = Column(Integer, primary_key=True)
    has_sub = Column(Boolean)
    is_active = Column(Boolean)
    created_datetime = Column(DATETIME)
    modified_datetime = Column(DATETIME)
    eng_name = Column(String(100))
    eng_plural = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))

    def __init__(self, dt_pattern=None, pattern1=None,
                 pattern2=None, serial=None, has_sub=None,
                 is_active=None, created_datetime=utc_now(),
                 modified_datetime=utc_now(), eng_name=None,
                 eng_plural=None, kor_name=None, jpn_name=None,
                 chn_name=None):
        self.dt_pattern = dt_pattern
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.serial = serial
        self.has_sub = has_sub
        self.is_active = is_active
        self.created_datetime = created_datetime
        self.modified_datetime = modified_datetime
        self.eng_name = eng_name
        self.eng_plural = eng_plural
        self.kor_name = kor_name
        self.jpn_name = jpn_name
        self.chn_name = chn_name

    def __repr__(self):
        return '<Nutrient %r>' % (self.eng_name)


class NutrientSet(Base):
    __tablename__ = 'nutrient_set'
    super_dt_pattern = Column(CHAR(1), primary_key=True)
    super_pattern1 = Column(CHAR(1), primary_key=True)
    super_pattern2 = Column(CHAR(2), primary_key=True)
    super_serial = Column(Integer, primary_key=True)
    sub_dt_pattern = Column(CHAR(1), primary_key=True)
    sub_pattern1 = Column(CHAR(1), primary_key=True)
    sub_pattern2 = Column(CHAR(2), primary_key=True)
    sub_serial = Column(Integer, primary_key=True)
    is_active = Column(Boolean)

    def __init__(self, super_dt_pattern=None,
                 super_pattern1=None,
                 super_pattern2=None,
                 super_serial=None,
                 sub_dt_pattern=None,
                 sub_pattern1=None,
                 sub_pattern2=None,
                 sub_serial=None, is_active=None):
        self.super_dt_pattern = super_dt_pattern
        self.super_pattern1 = super_pattern1
        self.super_pattern2 = super_pattern2
        self.super_serial = super_serial
        self.sub_dt_pattern = sub_dt_pattern
        self.sub_pattern1 = sub_pattern1
        self.sub_pattern2 = sub_pattern2
        self.sub_serial = sub_serial
        self.is_active = is_active

    def __repr__(self):
        return '<Nutrient Set>'


class Factor(Base):
    __tablename__ = 'factor'
    pattern1 = Column(CHAR(1), primary_key=True)
    pattern2 = Column(CHAR(1), primary_key=True)
    pattern3 = Column(CHAR(1), primary_key=True)
    pattern4 = Column(CHAR(1), primary_key=True)
    is_active = Column(Boolean)
    has_sub = Column(Boolean)
    eng_name = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))

    def __init__(self, pattern1=None, pattern2=None, pattern3=None,
                 pattern4=None, is_active=None, has_sub=None, eng_name=None,
                 kor_name=None, jpn_name=None, chn_name=None):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.pattern3 = pattern3
        self.pattern4 = pattern4
        self.is_active = is_active
        self.has_sub = has_sub
        self.eng_name = eng_name
        self.kor_name = kor_name
        self.jpn_name = jpn_name
        self.chn_name = chn_name

    def __repr__(self):
        return '<Factor>'


class FactorSet(Base):
    __tablename__ = 'factor_set'
    nutrient_dt_pattern = Column(CHAR(1), primary_key=True)
    nutrient_pattern1 = Column(CHAR(1), primary_key=True)
    nutrient_pattern2 = Column(CHAR(2), primary_key=True)
    nutrient_serial = Column(Integer, primary_key=True)
    factor_pattern1 = Column(CHAR(1), primary_key=True)
    factor_pattern2 = Column(CHAR(1), primary_key=True)
    factor_pattern3 = Column(CHAR(1), primary_key=True)
    factor_pattern4 = Column(CHAR(1), primary_key=True)
    is_active = Column(Boolean)
    unit_code = Column(CHAR(4))
    quantity = Column(REAL)

    def __init__(self, nutrient_dt_pattern=None,
                 nutrient_pattern1=None,
                 nutrient_pattern2=None, nutrient_serial=None,
                 factor_pattern1=None, factor_pattern2=None, factor_pattern3=None,
                 factor_pattern4=None, is_active=None, unit_code=None,
                 quantity=None):
        self.nutrient_dt_pattern = nutrient_dt_pattern
        self.nutrient_pattern1 = nutrient_pattern1
        self.nutrient_pattern2 = nutrient_pattern2
        self.nutrient_serial = nutrient_serial
        self.factor_pattern1 = factor_pattern1
        self.factor_pattern2 = factor_pattern2
        self.factor_pattern3 = factor_pattern3
        self.factor_pattern4 = factor_pattern4
        self.is_active = is_active
        self.unit_code = unit_code
        self.quantity = quantity

    def __repr__(self):
        return '<Factor Set>'


class NutrientPattern(Base):
    __tablename__ = 'nutrient_pattern'
    pattern1 = Column(CHAR(1), primary_key=True)
    pattern2 = Column(CHAR(2), primary_key=True)
    is_active = Column(Boolean)
    eng_name = Column(String(100))
    eng_plural = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))

    def __init__(self, pattern1=None, pattern2=None, is_active=None,
                 eng_name=None, eng_plural=None, kor_name=None,
                 jpn_name=None, chn_name=None):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.is_active = is_active
        self.eng_name = eng_name
        self.eng_plural = eng_plural
        self.kor_name = kor_name
        self.jpn_name = jpn_name
        self.chn_name = chn_name

    def __repr__(self):
        return '<nutrient Pattern>'


class DataPattern(Base):
    __tablename__ = 'data_pattern'
    pattern = Column(CHAR(1), primary_key=True)
    name = Column(String(100))
    is_active = Column(Boolean)

    def __init__(self, pattern=None, name=None, is_active=None):
        self.pattern = pattern
        self.name = pattern
        self.is_active = is_active

    def __repr__(self):
        return '<Data Pattern>'
