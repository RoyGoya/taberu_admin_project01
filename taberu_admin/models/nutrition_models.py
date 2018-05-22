# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

from sqlalchemy import Column, Integer, String, CHAR, Boolean, DATETIME, \
    REAL

from ..database import Base
from ..helpers.timezone_gen import utc_now


class Nutrition(Base):
    __tablename__ = 'nutrition'
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
        return '<Nutrition %r>' % (self.eng_name)


class NutritionSet(Base):
    __tablename__ = 'nutrition_set'
    super_nutrition_dt_pattern = Column(CHAR(1), primary_key=True)
    super_nutrition_pattern1 = Column(CHAR(1), primary_key=True)
    super_nutrition_pattern2 = Column(CHAR(2), primary_key=True)
    super_nutrition_serial = Column(Integer, primary_key=True)
    sub_nutrition_dt_pattern = Column(CHAR(1), primary_key=True)
    sub_nutrition_pattern1 = Column(CHAR(1), primary_key=True)
    sub_nutrition_pattern2 = Column(CHAR(2), primary_key=True)
    sub_nutrition_serial = Column(Integer, primary_key=True)
    is_active = Column(Boolean)

    def __init__(self, super_nutrition_dt_pattern=None,
                 super_nutrition_pattern1=None,
                 super_nutrition_pattern2=None,
                 super_nutrition_serial=None,
                 sub_nutrition_dt_pattern=None,
                 sub_nutrition_pattern1=None,
                 sub_nutrition_pattern2=None,
                 sub_nutrition_serial=None, is_active=None):
        self.super_nutrition_dt_pattern = super_nutrition_dt_pattern
        self.super_nutrition_pattern1 = super_nutrition_pattern1
        self.super_nutrition_pattern2 = super_nutrition_pattern2
        self.super_nutrition_serial = super_nutrition_serial
        self.sub_nutrition_dt_pattern = sub_nutrition_dt_pattern
        self.sub_nutrition_pattern1 = sub_nutrition_pattern1
        self.sub_nutrition_pattern2 = sub_nutrition_pattern2
        self.sub_nutrition_serial = sub_nutrition_serial
        self.is_active = is_active

    def __repr__(self):
        return '<Nutrition Set>'


class NutritionFactor(Base):
    __tablename__ = 'nutrition_factor'
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
        return '<Nutrition Factor>'


class NutritionFactorSet(Base):
    __tablename__ = 'nutrition_factor_set'
    nutrition_dt_pattern = Column(CHAR(1), primary_key=True)
    nutrition_pattern1 = Column(CHAR(1), primary_key=True)
    nutrition_pattern2 = Column(CHAR(2), primary_key=True)
    nutrition_serial = Column(Integer, primary_key=True)
    nf_pattern1 = Column(CHAR(1), primary_key=True)
    nf_pattern2 = Column(CHAR(1), primary_key=True)
    nf_pattern3 = Column(CHAR(1), primary_key=True)
    nf_pattern4 = Column(CHAR(1), primary_key=True)
    is_active = Column(Boolean)
    unit_code = Column(CHAR(4))
    quantity = Column(REAL)

    def __init__(self, nutrition_dt_pattern=None,
                 nutrition_pattern1=None,
                 nutrition_pattern2=None, nutrition_serial=None,
                 nf_pattern1=None, nf_pattern2=None, nf_pattern3=None,
                 nf_pattern4=None, is_active=None, unit_code=None,
                 quantity=None):
        self.nutrition_dt_pattern = nutrition_dt_pattern
        self.nutrition_pattern1 = nutrition_pattern1
        self.nutrition_pattern2 = nutrition_pattern2
        self.nutrition_serial = nutrition_serial
        self.nf_pattern1 = nf_pattern1
        self.nf_pattern2 = nf_pattern2
        self.nf_pattern3 = nf_pattern3
        self.nf_pattern4 = nf_pattern4
        self.is_active = is_active
        self.unit_code = unit_code
        self.quantity = quantity

    def __repr__(self):
        return '<Nutrition Factor Set>'


class NutritionPattern(Base):
    __tablename__ = 'nutrition_pattern'
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
        return '<Nutrition Pattern>'


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
