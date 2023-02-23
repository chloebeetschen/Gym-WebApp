# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config.from_pbject('config')
db = SQLAlchemy(app)


from app import views, models
