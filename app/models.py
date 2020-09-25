from sqlalchemy import Column, Integer, Float, Unicode, Boolean, DateTime, ForeignKey, BigInteger, TIMESTAMP

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import MetaData

Base = declarative_base(metadata=MetaData(schema='dbo'))



class NAV(Base):
    __tablename__ = "nav"
    id = Column(BigInteger, primary_key=True)
    scheme_name = Column(Unicode)
    scheme_code = Column(BigInteger, unique=True)
    nav = Column(BigInteger)
    created_date = Column(TIMESTAMP)
    last_updated = Column(TIMESTAMP, unique=True)

class SCHEME_DETAILS(Base):
    __tablename__ = "scheme_details"
    id = Column(BigInteger, primary_key=True)
    scheme_name = Column(Unicode)
    scheme_code = Column(BigInteger, unique=True)
    scheme_start_date_nav = Column(BigInteger)
    scheme_start_date = Column(TIMESTAMP)
    fund_house = Column(Unicode)
    scheme_category = Column(Unicode)
    scheme_type = Column(Unicode)

class SCHEME_CODES(Base):
    __tablename__ = "scheme_codes"
    scheme_code = Column(BigInteger, primary_key=True)
    created_date = Column(TIMESTAMP)
