from sqlalchemy import *;
from sqlalchemy.orm import sessionmaker;
import urllib
from models import Base;


def connect():

    params = urllib.quote_plus("DRIVER={SQL Server};SERVER=SIMON-HP\SQLEXPRESS;DATABASE=VoucherSystem;UID=sa;PWD=12345")
    engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
    Base.metadata.create_all(engine)
    Base.metadata.bind = engine
    Session = sessionmaker(bind=engine)
    return Session()