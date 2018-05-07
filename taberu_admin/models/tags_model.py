
from sqlalchemy import Column, Integer, String, CHAR, Boolean
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

    def __init__(self, dt_pattern=None, pattern=None, serial=None
                 , is_set=None, is_active=None, icon_code=None
                 , eng_name=None, kor_name=None, jpn_name=None
                 , chn_name=None):
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
