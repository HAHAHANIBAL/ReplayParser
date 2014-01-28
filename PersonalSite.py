#!/usr/bin/python
#-*- coding: utf-8 -*-

from flask import Flask
from flask import render_template
from flask import url_for

app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('login.html')

if __name__== '__main__':
    app.debug=True
    app.run(host='127.0.0.1')
