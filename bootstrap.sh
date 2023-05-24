#!/bin/sh


export FLASK_APP=./gradish/index.py
flask --app gradish/index run --debug