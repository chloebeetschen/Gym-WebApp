# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)  # Create an instance of the database object

migrate = Migrate(app, db, render_as_batch=True)
#sets flask_admin to use bootstarp and tells flask_admin which web app it is attached to
admin = Admin(app,template_mode='bootstrap4')

from app import views, models