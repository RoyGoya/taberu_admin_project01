# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

from sqlalchemy import Column, Integer, String, CHAR, Boolean, DATETIME

from ..database import Base
from ..helpers.timezone_gen import utc_now


class Nutrition(Base):
    __tablename__ = 'nutrition'
    dt_pattern = Column(CHAR(1), primary_key=True)
    nt_pattern1 = Column(CHAR(1), primary_key=True)
    nt_pattern2 = Column(CHAR(2), primary_key=True)
    serial = Column(Integer, primary_key=True)
    is_set = Column(Boolean)
    is_active = Column(Boolean)
    created_datetime = Column(DATETIME)
    modified_datetime = Column(DATETIME)
    eng_name = Column(String(100))
    eng_plural = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))

    def __init__(self, dt_pattern=None, nt_pattern1=None,
                 nt_pattern2=None, serial=None, is_set=None,
                 is_active=None, created_datetime=utc_now(),
                 modified_datetime=utc_now(), eng_name=None,
                 eng_plural=None, kor_name=None, jpn_name=None,
                 chn_name=None):
        self.dt_pattern = dt_pattern
        self.nt_pattern1 = nt_pattern1
        self.nt_pattern2 = nt_pattern2
        self.serial = serial
        self.is_set = is_set
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
    super_nutrition_nt_pattern1 = Column(CHAR(1), primary_key=True)
    super_nutrition_nt_pattern2 = Column(CHAR(2), primary_key=True)
    super_nutrition_serial = Column(Integer, primary_key=True)
    sub_nutrition_dt_pattern = Column(CHAR(1), primary_key=True)
    sub_nutrition_nt_pattern1 = Column(CHAR(1), primary_key=True)
    sub_nutrition_nt_pattern2 = Column(CHAR(2), primary_key=True)
    sub_nutrition_serial = Column(Integer, primary_key=True)
    is_active = Column(Boolean)

    def __init__(self, super_nutrition_dt_pattern=None,
                 super_nutrition_nt_pattern1=None,
                 super_nutrition_nt_pattern2=None,
                 super_nutrition_serial=None,
                 sub_nutrition_dt_pattern=None,
                 sub_nutrition_nt_pattern1=None,
                 sub_nutrition_nt_pattern2=None,
                 sub_nutrition_serial=None, is_active=None):
        self.super_nutrition_dt_pattern = super_nutrition_dt_pattern
        self.super_nutrition_nt_pattern1 = super_nutrition_nt_pattern1
        self.super_nutrition_nt_pattern2 = super_nutrition_nt_pattern2
        self.super_nutrition_serial = super_nutrition_serial
        self.sub_nutrition_dt_pattern = sub_nutrition_dt_pattern
        self.sub_nutrition_nt_pattern1 = sub_nutrition_nt_pattern1
        self.sub_nutrition_nt_pattern2 = sub_nutrition_nt_pattern2
        self.sub_nutrition_serial = sub_nutrition_serial
        self.is_active = is_active

    def __repr__(self):
        return '<Nutrition %r>' % (self.sub_nutrition_nt_pattern2)
