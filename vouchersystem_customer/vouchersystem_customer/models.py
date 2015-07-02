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
    Id = Column(Integer, primary_key = True)
    username = Column(String(128))
    name = Column(String(128))
    password = Column(String(128))
    area = Column(String(128))
    address1 = Column(String(128))
    address2 = Column(String(128))
    phone = Column(String(128))
    email = Column(String(128))
    logo = Column(String(128))

class Voucher(Base):
    __tablename__ = 'vouchers'
    Id = Column(Integer, primary_key = True)
    code = Column(String(128))
    type = Column(String(128))
    customer_name = Column(String(128))
    value = Column(Float)
    offset_issued = Column(Integer, default = offset/100)
    date_issued = Column(DATETIME(timezone=True), default = datetime.utcnow())
    date_expired = Column(DATETIME(timezone=True), default=datetime.utcnow() + timedelta(weeks=52))
    email = Column(String(128))
    staff_name = Column(String(128))
    payment_option = Column(String(128))
    voucher_state = Column(String(128))
    validated_date = Column(DATETIME(timezone=True), default=datetime.utcnow())
    hotel_Id = Column(Integer, ForeignKey('hotels.Id'))
    
class Purchase(Base):
    __tablename__ = 'purchases'
    Id = Column(Integer, primary_key = True)
    #voucher_code = Column(String(128))
    spent_at = Column(String(128))
    offset_purchase = Column(Integer, default = offset/100)
    purchase_date = Column(DATETIME(timezone=True), default=datetime.utcnow())
    current_value = Column(Float)
    amount_spent = Column(Float)
    amount_left = Column(Float)
    voucher_Id = Column(Integer, ForeignKey('vouchers.Id'))