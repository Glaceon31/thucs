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

#google mail api
from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.header import Header

def send(sender, receivers,title, message):
	msg = MIMEText(message,'plain','utf-8')

	me = ('%s<thucs@tsinghua.edu.cn>')%(Header(sender,'utf-8'))
	you = ';'.join(receivers)
	print sender

	msg['Subject'] = Header(title,'utf-8')
	msg['From'] = me
	msg['To'] = you
	msg["Accept-Language"]="zh-CN"
	msg["Accept-Charset"]="ISO-8859-1,utf-8"

	try:
		s = smtplib.SMTP('localhost')
		s.sendmail(me, receivers, msg.as_string())
		s.quit()
		print 'success'
		return True
	except:
		print 'fail'
		traceback.print_exc()
		return False

def gmail_send(sender, receivers,title, message):
	msg = MIMEText(message,'plain','utf-8')
	me = ('%s<thucs@tsinghua.edu.cn>')%(Header(sender,'utf-8'))
	#message = MIMEMultipart()
	msg['to'] = to
	msg['from'] = me
	msg['subject'] = Header(title,'utf-8')

	encoded = {'raw': base64.urlsafe_b64encode(msg.as_string())}
	try:
		message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
		print 'Message Id: %s' % message['id']
		return True
	except:
		print 'fail'
		traceback.print_exc()
		return False

@app.route('/mail', methods=['GET','POST'])
def mail():
	if request.form.has_key(u'提交'):
		data = immutabledict2dict(request.form)
		print data
		message = u"发送失败"
		try:
			if data['password'] != 'thucs':
				message = u"密码错误"
				assert 0 == 1
			receivers = [re.strip() for re in data['receiver'].split(';')]
			send(data['sender'],receivers, data['title'], data['message'])
			message = u"发送成功"
		except:
			traceback.print_exc()
		return render_template('mail.html',message = message)
	return render_template('mail.html',message = '')

	

