#!/bin/sh
source $(pipenv --venv)/bin/activate 
hypercorn stock.app:app 