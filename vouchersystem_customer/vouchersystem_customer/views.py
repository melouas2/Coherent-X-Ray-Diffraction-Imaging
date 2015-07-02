#Main file that renders html templates
from flask import Flask, url_for, request, session, render_template, redirect, flash;
from app import app;
import pyodbc;
from sqlalchemy import *;
from sqlalchemy.orm import sessionmaker;
import urllib;
from connection_string import connect;
from models import Voucher, Hotel, Purchase, Base;
from datetime import datetime, timedelta;
from random import randrange;
from flask_mail import Mail, Message;
from mail_pdf import allowed_file, create_pdf, send_voucher;
from werkzeug import secure_filename; 
from regexpressions import check_names;
import os;
import stripe;


# Email
mail = Mail(app)

# Connection string
db_session = connect()


@app.route('/', methods=['GET', 'POST'])
def home():
    return redirect(url_for('purchase_voucher'))


@app.route('/buy_voucher', methods=['GET', 'POST'])
def purchase_voucher():
    if request.method == 'GET':
        message = ""
        return get_hotel(message)
    
    elif request.method == 'POST':
        
        email = request.form['Email']
        print(email)
        if email == "":
            message = "Please enter a valid email"
            return get_hotel(message)
        else:
            print("In else")
            generate_code = True
            short_name = ""
            first_name = request.form['FirstName']
            last_name = request.form['LastName']
            if check_names(first_name, last_name):
                print("This works")
                for i in request.form['Hotel'].upper().split():
                    short_name += i[0]
                    while generate_code:
                        voucherId_generate = randrange(100000, 999999)
                        count = db_session.query(Voucher).filter(Voucher.Id == voucherId_generate).scalar()
                        if count is None:
                            print("VoucherId_generate does NOT already exist")
                            generate_code = False
                
                Id = voucherId_generate
                code = short_name + "O" + "{0}".format(voucherId_generate)
                type = request.form['VoucherType']
                customer_name = first_name + " " + last_name
                value = request.form['Amount']
                payment_option = "Online Payment"
                print("Trying get_ID")
                get_Id = db_session.query(Hotel.Id).filter(Hotel.name == request.form['Hotel']).first()
                hotel_Id = get_Id[0]
                print(hotel_Id)
                create_voucher(Id, code, type, customer_name, value, email, payment_option, hotel_Id)
                send_voucher(code, email, request.form['Hotel'], hotel_Id)
                message = "Thank you for your purchase"
                print(message)
                return get_hotel(message)
            else:
                message = "Incorrect customer name entered"
                return get_hotel(message)

def get_hotel(message):
    s = select([Hotel])
    result = db_session.execute(s)
    all_rows = [dict(Hotel=row[2]) for row in result.fetchall()]
    
    #Prevents same hotel appearring more than once
    rows = [dict(tupleized) for tupleized in set(tuple(item.items()) for item in all_rows)]
    if message == "":
        return render_template("Home.html", rows = rows)
    else:
        return render_template("Home.html", rows = rows, message = message)

def create_voucher(voucher_Id, code, type, customer_name, value, email, payment_option, hotel_Id):
    print("tring voucher")
    v = Voucher(
            Id = voucher_Id,
            code = code,
            type = type,
            customer_name = customer_name,
            value = value,
            email = email,
            payment_option = payment_option,
            voucher_state = "Active",
            hotel_Id = hotel_Id)
    db_session.add(v)
    db_session.commit()


               