from flask import Flask, url_for, request, session, render_template, redirect, flash;
from app import app;
import pyodbc;
from sqlalchemy import *;
from sqlalchemy.orm import sessionmaker;
import urllib
from models import Voucher, Hotel, Base;
from datetime import datetime, timedelta;
from random import randrange;
from flask_mail import Mail, Message;
from pdfs import create_pdf;
from werkzeug import secure_filename; 
import re;
import os;
import stripe;


#EMAIL SETTINGS
app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'alkimiivoucher@gmail.com',
	MAIL_PASSWORD = 'Voucher_System'
	)
mail = Mail(app)

params = urllib.quote_plus("DRIVER={SQL Server};SERVER=SIMON-HP\SQLEXPRESS;DATABASE=VoucherSystem;UID=sa;PWD=12345")
engine = create_engine("mssql+pyodbc:///?odbc_connect=%s" % params)
Base.metadata.bind = engine
Session = sessionmaker(bind=engine)
db_session = Session()


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        s = select([Hotel])
        result = db_session.execute(s)
        all_rows = [dict(Hotel=row[1]) for row in result.fetchall()]

        #Prevents same hotel appearring more than once  
        rows = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in all_rows)]
        return render_template("Home.html", rows = rows)
    elif request.method == 'POST':
        email = request.form['Email']

        if email == "":
            error = "Please enter a valid email"
            return render_template("Home.html", error = error)
        else:
            generate_code = True
            short_name = ""
            #staff_name = request.form['StaffName']
            #correct_staff_name = re.match('^[a-z ]{5,100}$', staff_name, re.I)

            #if correct_staff_name:
            for i in request.form['Hotel'].upper().split():
                        short_name += i[0]
            while generate_code:
                voucherId_generate = randrange(100000, 999999)
                count = db_session.query(Voucher).filter(Voucher.voucher_Id == voucherId_generate).scalar()
                if count is None:
                    print("VoucherId_generate does NOT already exist")
                    generate_code = False
            code = short_name + "O" + "{0}".format(voucherId_generate)
            print(code)
            v = Voucher(
                voucher_Id = voucherId_generate,
                voucher_code = code,
                voucher_type = request.form['VoucherType'],
                value = request.form['Amount'],
                delivery_option = request.form['DeliveryOption'],
                #staff_name = staff_name,
                payment_option = "Online Payment",
                voucher_state = "Active",
                hotel_name = request.form['Hotel'])
            db_session.add(v)
            db_session.commit()
            
            for voucher in db_session.query(Voucher).filter(Voucher.voucher_code == code):
                msg = Message(
                        'Voucher Issue',
	                sender='alkimiivoucher@gmail.com',
	                recipients=
                        [email])
                msg.body = """Thank you for your purchase please see-attached your voucher below-\n 
                                Kind regards, \n \n
                                The {0}""".format(request.form['Hotel'])
                pdf = create_pdf(render_template('VoucherPDF.html', code = voucher.voucher_code, type = voucher.voucher_type, value = '%.2f' % voucher.value, issue_date = (voucher.date_issued + timedelta(hours=voucher.offset_issued)).strftime("%H:%M %d-%m-%Y"), expiry_date = (voucher.date_expired + timedelta(hours=voucher.offset_issued)).strftime("%H:%M %d-%m-%Y"), hotel_name = request.form['Hotel']))
                msg.attach("voucher.pdf", "application/pdf", pdf.getvalue())
                mail.send(msg)
                error = "Thank you for your purchase"
                return "<h2>Thank you for your purchase</h2>"

#@app.route('/vouchers', methods=['GET', 'POST'])
#def add_voucher():
#    if request.method == 'GET':
#        #hotel = request.args.get("hotel")
#        cents = request.args.get("amount")
#        amount = int(cents) * 100
#        print(amount)
#        s = select([Hotel])
#        result = db_session.execute(s)
#        all_rows = [dict(Hotel=row[1]) for row in result.fetchall()]

#        #Prevents same hotel appearring more than once  
#        rows = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in all_rows)]
#        return render_template("Home.html", rows = rows, amount = "{0}".format(amount))
    
#    elif request.method == 'POST':
#        email = request.form['Email']

#        if email == "":
#            error = "Please enter a valid email"
#            return render_template("Home.html", error = error)
#        else:
#            generate_code = True
#            short_name = ""
#            #staff_name = request.form['StaffName']
#            #correct_staff_name = re.match('^[a-z ]{5,100}$', staff_name, re.I)

#            #if correct_staff_name:
#            for i in request.form['Hotel'].upper().split():
#                        short_name += i[0]
#            while generate_code:
#                voucherId_generate = randrange(100000, 999999)
#                count = db_session.query(Voucher).filter(Voucher.voucher_Id == voucherId_generate).scalar()
#                if count is None:
#                    print("VoucherId_generate does NOT already exist")
#                    generate_code = False
#            code = short_name + "O" + "{0}".format(voucherId_generate)
#            print(code)
#            v = Voucher(
#                voucher_Id = voucherId_generate,
#                voucher_code = code,
#                voucher_type = request.form['VoucherType'],
#                value = request.form['Amount'],
#                delivery_option = request.form['DeliveryOption'],
#                #staff_name = staff_name,
#                payment_option = "Online Payment",
#                voucher_state = "Active",
#                hotel_name = request.form['Hotel'])
#            db_session.add(v)
#            db_session.commit()
            
#            for voucher in db_session.query(Voucher).filter(Voucher.voucher_code == code):
#                msg = Message(
#                        'Voucher Issue',
#	                sender='alkimiivoucher@gmail.com',
#	                recipients=
#                        [email])
#                msg.body = """Thank you for your purchase please see-attached your voucher below-\n 
#                                Kind regards, \n \n
#                                The {0}""".format(request.form['Hotel'])
#                pdf = create_pdf(render_template('VoucherPDF.html', code = voucher.voucher_code, type = voucher.voucher_type, value = '%.2f' % voucher.value, issue_date = (voucher.date_issued + timedelta(hours=voucher.offset_issued)).strftime("%H:%M %d-%m-%Y"), expiry_date = (voucher.date_expired + timedelta(hours=voucher.offset_issued)).strftime("%H:%M %d-%m-%Y"), hotel_name = request.form['Hotel']))
#                msg.attach("voucher.pdf", "application/pdf", pdf.getvalue())
#                mail.send(msg)
#                error = "Thank you for your purchase"
#                return "<h2>Thank you for your purchase</h2>"

#            #else:
#            #    error = "Please enter a correct staff name"
#            #    return "<h2>Thank you for your purchase</h2>"
