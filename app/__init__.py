# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

app = Flask(__name__)

# Include configuration file:
app.config.from_object('config')

# Create instance of database object
db = SQLAlchemy(app)

# Allow for columns to be added or dropped in db
migrate = Migrate(app, db, render_as_batch=True)

# Set up flask admin to manage db
admin = Admin(app, template_mode='bootstrap4')

from app import views, models