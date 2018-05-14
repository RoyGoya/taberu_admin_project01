# SQLAlchemy
# http://flask.pocoo.org/docs/0.12/patterns/sqlalchemy/

from sqlalchemy import Column, Integer, String, CHAR, Boolean, ForeignKey
from ..database import Base


class Tag(Base):
    __tablename__ = 'tag'
    dt_pattern = Column(CHAR(1), primary_key=True)
    pattern = Column(CHAR(1), primary_key=True)
    serial = Column(Integer, primary_key=True)
    is_set = Column(Boolean)
    is_active = Column(Boolean)
    icon_code = Column(CHAR(6))
    eng_name = Column(String(100))
    kor_name = Column(String(100))
    jpn_name = Column(String(100))
    chn_name = Column(String(100))

    def __init__(self, dt_pattern=None, pattern=None, serial=None,
                 is_set=None, is_active=None, icon_code=None,
                 eng_name=None, kor_name=None, jpn_name=None,
                 chn_name=None):
        self.dt_pattern = dt_pattern
        self.pattern = pattern
        self.serial = serial
        self.is_set = is_set
        self.is_active = is_active
        self.icon_code = icon_code
        self.eng_name = eng_name
        self.kor_name = kor_name
        self.jpn_name = jpn_name
        self.chn_name = chn_name

    def __repr__(self):
        return '<Tag %r>' % (self.eng_name)


class TagSet(Base):
    __tablename__ = 'tag_set'
    super_tag_dt_pattern = Column(CHAR(1), ForeignKey('tag.dt_pattern'), primary_key=True)
    super_tag_pattern = Column(CHAR(1), ForeignKey('tag.pattern'), primary_key=True)
    super_tag_serial = Column(Integer, ForeignKey('tag.serial'), primary_key=True)
    is_active = Column(Boolean)
    sub_tag_dt_pattern = Column(CHAR(1), primary_key=True)
    sub_tag_pattern = Column(CHAR(1), primary_key=True)
    sub_tag_serial = Column(Integer, primary_key=True)


    def __init__(self, super_tag_dt_pattern=None, super_tag_pattern=None,
                 super_tag_serial=None, is_active=None,
                 sub_tag_dt_pattern=None, sub_tag_pattern=None,
                 sub_tag_serial=None):
        self.super_tag_dt_pattern = super_tag_dt_pattern
        self.super_tag_pattern = super_tag_pattern
        self.super_tag_serial = super_tag_serial
        self.is_active = is_active
        self.sub_tag_dt_pattern = sub_tag_dt_pattern
        self.sub_tag_pattern = sub_tag_pattern
        self.sub_tag_serial = sub_tag_serial

    def __repr__(self):
        return '<TagSet %r>' % (self.super_tag_serial)
