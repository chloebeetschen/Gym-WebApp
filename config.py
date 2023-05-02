# Configuring SQLite
# Informs where the sqlalchemy will put the database file.
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# Configuration for forms 
# Determines if CSRF is needed
WTF_CSRF_ENABLED = True

# Key used to create secure token, should be something secretive
SECRET_KEY = 'group6-secret-key'
# Could use:
# import secrets
# secretKey = secrets.token_hex()