from sqlalchemy import Column, Integer, String, CHAR, Boolean, DATETIME, \
    REAL

from ..database import Base


class Unit(Base):
    __tablename__ = 'unit'
    pattern = Column(CHAR(2), primary_key=True)
    serial = Column(Integer, primary_key=True)
    is_active = Column(Boolean)
    symbol = Column(String(10))
    eng_name = Column(String(100))

    def __init__(self, pattern=None, serial=None, is_active=None,
                 symbol=None, eng_name=None):
        self.pattern = pattern
        self.serial = serial
        self.is_active = is_active
        self.symbol = symbol
        self.eng_name = eng_name

    def __repr__(self):
        return '<{0}>'.format(self.__class__.__name__)
