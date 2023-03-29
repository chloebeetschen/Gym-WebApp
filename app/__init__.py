# This runs when the package loads
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
import logging
import os
import stripe


stripe_keys = {
    'secretKey' : os.environ['TEST_SECRET_KEY'],
    'publicKey' : os.environ['TEST_PUBLISH_KEY']
}

stripe.api_key = stripe_keys['secretKey']

logging.basicConfig(filename='squad6.log', format='%(levelname)s | %(asctime)s | %(message)s', datefmt='%d/%m/%Y %H:%M:%S', level=logging.DEBUG)

app = Flask(__name__)

app.config.from_object('config')

with app.app_context():
    db = SQLAlchemy(app)  # Create an instance of the database object

    migrate = Migrate(app, db, render_as_batch=True)  # Lets you change tables
    # sets flask_admin to use bootstrap and tells flask_admin which web app it is attached to
    admin = Admin(app, template_mode='bootstrap4')
    
    

from app import views, models, db
