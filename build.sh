#!/bin/bash

# Stripe payment API keys
export TEST_SECRET_KEY=sk_test_51MqFY2LpcMacjDf9yRBh0SzcUGF0btlDkKiPV0MvQwrfKcC2ORXEdOGtyksgbeBmZ2rKCAknKrwTp7XpsYSkB5wT00AgHMZlv5
export TEST_PUBLISH_KEY=pk_test_51MqFY2LpcMacjDf9ZlpjrggbpqtMLahRRh7LGq5UPnTldWajaFCKWLxtDnvMLoF8yOR5xmNUj6EQJVS1RmsMHDUL00QT94jdFT

# Clean mode
if [ "$1" == "--clean" ]; then
  export FLASK_APP=run.py
  export FLASK_DEBUG=1
  rm -r -f migrations
  rm *.db
  flask db init
  flask db migrate -m "Initial migration"
  flask db upgrade
else
  # Normal mode
  export FLASK_APP=run.py
  export FLASK_DEBUG=1
fi

#port to run the web application on
flask run --port=5002


#010101  010101  010101  10101
#01  01  01  01  01  01 01
#010101  010101  010101 01  111
#01  01  01  01  10  01 01   00
#10  01  01  01  01  01  11001
