#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.debug = True

import pymongo
import traceback
from pymongo import MongoClient

client = MongoClient(connect=False)

db = client.thucs


@app.route('/register')
def register():
	return render_template('register.html')

@app.route('/')
@app.route('/login')
def login():
	return render_template('login.html')

@app.route('/mainpage')
def mainpage():
	return render_template('mainpage.html')


@app.route('/modifyinfo')
def modify():
	return render_template('modifyinfo.html')

@app.route('/modifypassword')
def modifypassword():
	return render_template('modifypassword.html')

@app.route('/scholarship')
def scholarship():
	return render_template('scholarship.html')

@app.route('/scholarshiplist')
def scholarshiplist():
	slist=getscholarshiplist()
	return render_template('scholarshiplist.html', slist=slist)

@app.route('/scholarshipcheck/<sid>')
def scholarshipcheck(sid):
	info = getscholarshipinfo(sid)
	return render_template('scholarcheck.html', info = info)

@app.route('/fonts/<path>')
def fonts(path):
	return redirect('/static/fonts/'+path)

from user import *
from scholarship import *

if __name__ == '__main__':
    app.run('0.0.0.0', port = 7654)
