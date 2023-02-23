from flask import render_template
from app import app
from .forms import *

@app.route('/')
def index():
    return '<h1>This is working.</h1>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = Login()
    return render_template('login.html',
                            form = form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = Register()
    return render_template('register.html',
                            form = form)
