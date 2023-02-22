from flask import render_template, flash
from app import app
from .forms import PaymentForm

@app.route('/')
def index():
    return '<h1>This is working.</h1>'

#Register Page
@app.route('/paymentForm', methods=['GET', 'POST'])
def paymentForm():
    form = PaymentForm()
    # Add data to database on submit:
    if form.validate_on_submit():
        flash('Payment details registered')
    return render_template('paymentForm.html', title='payment form', form=form)
