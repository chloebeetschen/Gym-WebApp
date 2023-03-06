# Configuring SQLite
# Informs where the sqlalchemy will put the database file.
import os

basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = True

# configuration for forms 
# determines if CSRF is needed
WTF_CSRF_ENABLED = True

# key used to create secure token
# Key should be something secretive.
# Can use:
# import secrets
# secretKey = secrets.token_hex()
SECRET_KEY = 'group6-secret-key'