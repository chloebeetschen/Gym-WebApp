#!/bin/bash

export FLASK_APP=run.py
export FLASK_DEBUG=1
rm -r -f migrations
rm *.db
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
flask run