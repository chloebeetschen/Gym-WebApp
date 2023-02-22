# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#create instance of database object
#db = SQLAlchemy(app)

app = Flask(__name__)

# include configuration file:
app.config.from_object('config')

# allow for columns to be added or dropped in db
#migrate = Migrate(app, db, render_as_batch=True)

from app import views#, models