# create database
from config import SQLALCHEMY_DATABASE_URI
from app import app, db 
import os.path

db.create_all()
