from flask import render_template, flash
from app import app, db, admin, models
from .forms import PaymentForm
from flask_admin.contrib.sqla import ModelView
from .models import PaymentCard

# Register table models with flask admin
admin.add_view(ModelView(PaymentCard, db.session))

@app.route('/')
def index():
    return render_template('home.html', title='home')


#Payment Form page
@app.route('/paymentForm', methods=['GET', 'POST'])
def paymentForm():
    form = PaymentForm()
    # Add data to database on submit:
    if form.validate_on_submit():
        # Create Payment Card field with entered details
        newCard = models.PaymentCard(cardName=form.cName.data, cardNum=form.cNum.data, cardExpDate=form.cExpDate.data, cardCVV=form.cCVV.data)
        # Add new card entry to database and commit
        db.session.add(newCard)
        db.session.commit()

        flash('Payment details registered')
    return render_template('paymentForm.html', title='Payment Form', form=form)
