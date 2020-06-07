from flask import Flask


"""
This script runs the application using a development server.
It contains the definition of routes and views for the application.
"""

app = Flask(__name__)

from app import controllers
# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app






