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

import httplib2
import os

# Import the email modules we'll need
from email.mime.text import MIMEText
from email.header import Header
import base64
import traceback
import codecs
import string
#init the gmail api

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
#SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
SCOPES = 'https://www.googleapis.com/auth/gmail.send'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'

members = open('info.txt', 'r').read().split('\n')[1:-1]
members = [i.split('\t') for i in members]
print members[0]
print members[-1]


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials



def create_message(sender, to, subject, message_text):
    """Create a message for an email.

    Args:
        sender: Email address of the sender.
        to: Email address of the receiver.
        subject: The subject of the email message.
        message_text: The text of the email message.

    Returns:
        An object containing a base64url encoded email object.
    """
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string())}

def send_message(service, user_id, message):
    """Send an email message.

    Args:
        service: Authorized Gmail API service instance.
        user_id: User's email address. The special value "me"
        can be used to indicate the authenticated user.
        message: Message to be sent.

    Returns:
        Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message)
               .execute())
        print 'Message Id: %s' % message['id']
        return message
    except:
        traceback.print_exc()

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
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    message = create_message('grit394728923@gmail.com','grit31@126.com','gmail API test','test')
    m = send_message(service, 'grit394728923@gmail.com', message)

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
			gmail_send(data['sender'],receivers, data['title'], data['message'])
			message = u"发送成功"
		except:
			traceback.print_exc()
		return render_template('mail.html',message = message)
	return render_template('mail.html',message = '')


def getmaillist(member):
    result = ['thucs_graduate@googlegroups.com']
    try:
        year = string.atoi(member[3][0:4])
    except:
        print member
        return result
    if year <= 2011:
        result.append('thucs_11@googlegroups.com')
    elif year <= 2016:
        result.append('thucs_'+str(year-2000)+'@googlegroups.com')
    return result

@app.route('/getmailaddresses/<maillist>', methods=['GET','POST'])
def getmailaddresses(maillist):
    result = ''
    for i in members:
        if maillist in getmaillist(i):
            result += i[10]+','
    tmp = open('address.txt','w')
    tmp.write(result)
    tmp.close()
    return result

@app.route('/getmembers/<maillist>', methods=['GET','POST'])
def getmembers(maillist):
    result = []
    for i in members:
        if maillist in getmaillist(i):
            result += [[i[3],i[4],i[10]]]
    return json.dumps(result)

@app.route('/maillist', methods=['GET','POST'])
def maillist():
    return render_template('maillist.html',message = '')
