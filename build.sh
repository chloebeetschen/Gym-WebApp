#!/bin/bash

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

flask run --port=5012
