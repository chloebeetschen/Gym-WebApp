# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin

import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

admin = Admin(app, template_mode='bootstrap4')

migrate = Migrate(app, db)

from app import views, models
