import os
from flask import Flask, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)

# Key for Forms
app.config['SECRET_KEY'] = 'mysecretkey'

# Database Setup
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
Migrate(app,db)


# Import and Register Blueprints
from sabi.devices.views import devices_blueprint
app.register_blueprint(devices_blueprint, url_prefix='/devices')

from sabi.core.views import core_blueprint
app.register_blueprint(core_blueprint)

from sabi.error_pages.handlers import error_pages
app.register_blueprint(error_pages)
