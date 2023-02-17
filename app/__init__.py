# This runs when the package loads
from flask import Flask

app = Flask(__name__)
from app import views
