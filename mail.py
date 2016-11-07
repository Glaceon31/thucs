#coding:utf-8
# Import smtplib for the actual sending function
from flask import Flask, render_template, request, redirect, url_for
from app import app, db
import traceback
import json
import datetime
import random
from tools import *
import smtplib

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.header import Header

def send(receivers, title, message):
	msg = MIMEText(message,'plain','utf-8')

	me = 'thucs@tsinghua.edu.cn'
	#you = 'grit31@126.com'

	msg['Subject'] = Header(title,'utf-8')
	msg['From'] = Header("清华大学计算机系研团",'utf-8')
	#msg['To'] = you

	try:
		s = smtplib.SMTP('localhost')
		s.sendmail(me, receivers, msg.as_string())
		s.quit()
		print 'success'
		return True
	except:
		print 'fail'
		return False

@app.route('/mail', methods=['GET','POST'])
def mail():
	if request.form.has_key(u'提交'):
		data = immutabledict2dict(request.form)
		print data
		return 
		message = u"发送失败"
		try:
			receivers = [re.strip() for re in data[receiver].split(';')]
			send(receivers, data['title'], data['message'])
			message = u"发送成功"
		except:
			traceback.print_exc()
		return render_template('mail.html',message = message)
	return render_template('mail.html',message = '')

	
