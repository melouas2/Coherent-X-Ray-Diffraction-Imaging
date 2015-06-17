
"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

from flask import Flask
from flask_mail import Mail
import os
app = Flask(__name__)
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

from views import *
from models import *



if __name__ == '__main__':
    app.secret_key = 'secret_key'
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT, debug=True)
