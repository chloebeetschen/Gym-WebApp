# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)  # Create an instance of the database object

migrate = Migrate(app, db, render_as_batch=True)

from app import views, models
