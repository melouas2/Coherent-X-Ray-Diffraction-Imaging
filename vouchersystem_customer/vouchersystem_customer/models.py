#This python file builds all sql tables using sqlalchemy
import pyodbc;
from sqlalchemy import *;
from sqlalchemy.orm import sessionmaker;
from sqlalchemy.ext.declarative import declarative_base;
import urllib;
from datetime import datetime, timedelta;
from dateutil import tz;

#Proper method of getting accurate local time
from_zone = tz.tzutc()
to_zone = tz.tzlocal()
utc = datetime.utcnow()
utc = utc.replace(tzinfo = from_zone)
central = utc.astimezone(to_zone)
offset = int(central.strftime("%z")) 
Base = declarative_base()

#Classes for sql tables

class Hotel(Base):
    __tablename__ = 'hotels'
    hotel_Id = Column(String(128), primary_key = True)
    hotel_name = Column(String(128))
    password = Column(String(128))
    area = Column(String(128))
    address1 = Column(String(128))
    address2 = Column(String(128))
    phone = Column(String(128))
    email = Column(String(128))
    logo = Column(String(128))

class Voucher(Base):
    __tablename__ = 'vouchers'
    voucher_Id = Column(Integer, primary_key = True)
    voucher_code = Column(String(128))
    voucher_type = Column(String(128))
    value = Column(Float)
    offset_issued = Column(Integer, default = offset/100)
    date_issued = Column(DATETIME(timezone=True), default = datetime.utcnow())
    date_expired = Column(DATETIME(timezone=True), default=datetime.utcnow() + timedelta(weeks=52))
    delivery_option = Column(String(128))
    staff_name = Column(String(128))
    payment_option = Column(String(128))
    voucher_state = Column(String(128))
    validated_date = Column(DATETIME(timezone=True), default=datetime.utcnow())
    hotel_name = Column(String(128))
    

    #def __init__(self, )

#Connection string to sql environment
params = urllib.quote_plus("DRIVER={SQL Server};SERVER=SIMON-HP\SQLEXPRESS;DATABASE=VoucherSystem;UID=sa;PWD=12345")
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
Base.metadata.create_all(engine)