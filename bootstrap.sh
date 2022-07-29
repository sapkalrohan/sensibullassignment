#!/bin/sh
export FLASK_APP=./stock/app.py
source $(pipenv --venv)/bin/activate 
flask run --host=0.0.0.0 --port=5000