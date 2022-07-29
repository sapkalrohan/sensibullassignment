#!/bin/sh
# export FLASK_APP=./stock/app.py
# export QUART_APP=stock.app
source $(pipenv --venv)/bin/activate 
# flask run --host=0.0.0.0 --port=19093
# quart run --host=0.0.0.0 --port=19093
hypercorn stock.app --bind '127.0.0.1:19093'