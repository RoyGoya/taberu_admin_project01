from sqlalchemy import Column, String, CHAR, Boolean, REAL

from ..database import Base


class UnitCommon(Base):
    __tablename__ = 'unit_common'
    pattern1 = Column(CHAR(2), primary_key=True)
    pattern2 = Column(CHAR(2), primary_key=True)
    is_active = Column(Boolean)
    symbol = Column(String(30))
    eng_name = Column(String(100))

    def __init__(self, pattern1=None, pattern2=None, is_active=None,
                 symbol=None, eng_name=None):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.is_active = is_active
        self.symbol = symbol
        self.eng_name = eng_name

    def __repr__(self):
        return '<{0}>'.format(self.__class__.__name__)


class UnitUSCS(Base):
    __tablename__ = 'unit_uscs'
    pattern1 = Column(CHAR(2), primary_key=True)
    pattern2 = Column(CHAR(2), primary_key=True)
    co_pattern = Column(CHAR(2), primary_key=True)
    is_active = Column(Boolean)
    symbol = Column(String(30))
    eng_name = Column(String(100))
    uscs_to_common = Column(REAL)
    common_to_uscs = Column(REAL)

    def __init__(self, pattern1=None, pattern2=None, co_pattern=None,
                 is_active=None, symbol=None, eng_name=None,
                 uscs_to_common=None, common_to_uscs=None):
        self.pattern1 = pattern1
        self.pattern2 = pattern2
        self.co_pattern = co_pattern
        self.is_active = is_active
        self.symbol = symbol
        self.eng_name = eng_name
        self.uscs_to_common = uscs_to_common
        self.common_to_uscs = common_to_uscs

    def __repr__(self):
        return '<{0}>'.format(self.__class__.__name__)
