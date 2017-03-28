#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from werkzeug import secure_filename

app = Flask(__name__)
app.debug = True
import traceback
import json
import datetime
import random
from tools import *
import re
import datetime
import os
import pymongo
import traceback
from pymongo import MongoClient
client = MongoClient(connect=False)

db = client.thucs2017
userdb = db.user
logdb = db.log
notifydb = db.notify
gongshidb = db.gongshi

@app.route('/uploadnotify', methods=['GET', 'POST'])
def uploadnotify():
	return render_template('uploadnotify.html')

@app.route('/uploadingnotify', methods=['GET', 'POST'])
def uploadingnotify():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	try:
		if data['pass'] != '11':
			return u'密码错误'
		file = request.files['file']
		file.save(os.path.join('notify', file.filename))
		notify = {'time':datetime.datetime.now(),'description':data['description'],'filename':file.filename}
		notifydb.insert_one(notify)
		return u'上传成功'
	except:
		traceback.print_exc()
		return u'上传失败'

@app.route('/uploadgongshi', methods=['GET', 'POST'])
def uploadgongshi():
	return render_template('uploadgongshi.html')

@app.route('/uploadinggongshi', methods=['GET', 'POST'])
def uploadinggongshi():
	jsondata = request.form
	data = immutabledict2dict(jsondata)
	result = {'success' :0}
	try:
		if data['pass'] != '11':
			return u'密码错误'
		file = request.files['file']
		file.save(os.path.join('gongshi', file.filename))
		gongshi = {'time':datetime.datetime.now(),'description':data['description'],'filename':file.filename}
		gongshidb.insert_one(gongshi)
		return u'上传成功'
	except:
		traceback.print_exc()
		return u'上传失败'

@app.route('/scholarshiplist/')
def scholarshiplist():
	return render_template('scholarshiplist.html')

@app.route('/scholarshipview/<username>', methods=['GET', 'POST'])
def scholarshipcheck(username):
	print request.form
	if request.form.has_key(u'提交'):
		print 'admin modifying'

		#print request.form
		data = immutabledict2dict(request.form)
		print 'pass',data['pass']
		if data['pass'] != '11':
			print 'wrong pass'
			return render_template('scholarshipadminview.html', username=username, message=u'密码错误')
		message = u"提交失败"
		try:
			#print data
			tmp = userdb.find_one({'username': data['username']})
			logdata = {}
			logdata['action'] = 'adminmodify'
			logdata['scholarshipinfo'] = json.dumps(data)
			logdata['username'] = tmp['username']
			logdata['ip'] = request.remote_addr
			logdata['time'] = datetime.datetime.now()
			logdb.insert(logdata)	
			userdb.update_one({'username':data['username']},{'$set':{'reported':data['reported']}})
			userdb.update_one({'username':data['username']},{'$set':{'zige':data['zige']}})
			del data['pass']
			userdb.update_one({'username':data['username']},{'$set':{'scholarshipinfo':json.dumps(data)}})
			message = u"提交成功"
			return render_template('scholarshipadminview.html', username=username, message=message)
		except:
			traceback.print_exc()
	return render_template('scholarshipadminview.html', username=username)

from adminscholarship import *

if __name__ == '__main__':
	app.run('0.0.0.0', port = 5735)