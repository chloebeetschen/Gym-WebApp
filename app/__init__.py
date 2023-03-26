# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_migrate import Migrate
from flask_admin import Admin
import logging


app = Flask(__name__)

app.config.from_object('config')

with app.app_context():
    db = SQLAlchemy(app)  # Create an instance of the database object

    migrate = Migrate(app, db, render_as_batch=True)  # Lets you change tables
    # sets flask_admin to use bootstrap and tells flask_admin which web app it is attached to
    admin = Admin(app, template_mode='bootstrap4')

from app import views, models, db
