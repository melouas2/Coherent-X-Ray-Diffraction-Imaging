#Convert html to pdf file
from flask import render_template;
from flask_mail import Mail, Message;
from datetime import datetime, timedelta;
from models import Voucher, Hotel, Purchase, Base;
from connection_string import connect;
from app import app;
from xhtml2pdf import pisa;
from cStringIO import StringIO

db_session = connect()
mail = Mail(app)

UPLOAD_FOLDER = './static/logos'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG', 'pdf'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.update(
	DEBUG=True,
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = 'alkimiivoucher@gmail.com',
	MAIL_PASSWORD = 'Voucher_System'
	)

def allowed_file(filename):
    print("In function")
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def create_pdf(pdf_data):
    pdf = StringIO()
    pisa.CreatePDF(StringIO(pdf_data.encode('utf-8')), pdf)
    return pdf


def send_voucher(code, email, hotel_name, hotel_Id):

    for voucher in db_session.query(Voucher).filter(Voucher.code == code):
            for hotel in db_session.query(Hotel).filter(Hotel.Id == hotel_Id):
                print(hotel.logo)
                msg = Message(
                        'Voucher Issue',
	                sender='alkimiivoucher@gmail.com',
	                recipients=
                        [email])
                msg.body = """Dear {0},\n\nThank you for your purchase, please see-attached your voucher below.\n Kind regards,\n\nThe {1}""".format(voucher.customer_name, hotel_name)
                pdf = create_pdf(render_template('VoucherPDF.html', code = voucher.code,
                                                 customer =voucher.customer_name,
                                                 type = voucher.type,
                                                 value = '%.2f' % voucher.value,
                                                 issue_date = (voucher.date_issued + timedelta(hours=voucher.offset_issued)).strftime("%d-%m-%Y"),
                                                 expiry_date = (voucher.date_expired + timedelta(hours=voucher.offset_issued)).strftime("%d-%m-%Y"),
                                                 hotel_name = hotel_name, hotel_logo = hotel.logo))
                msg.attach("voucher.pdf", "application/pdf", pdf.getvalue())
                mail.send(msg)

