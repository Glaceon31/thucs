#-*- coding: utf-8 -*-
from flask import Flask, render_template, request, redirect, url_for
from app import app, db
import traceback
import json
import datetime
import random
from tools import *
#from user import getuserinfo
import re

userdb = db.user

@app.route('/scholarshipapply', methods=['GET','POST'])
def scholarshipapply():
    #print request.form
    if request.form.has_key(u'提交'):
        #print request.form
        data = immutabledict2dict(request.form)
        message = u"提交失败"
        try:
            print data
            userdb.update_one({'username':data['username']},{'$set':{'scholarshipinfo':json.dumps(data)}})
            message = u"提交成功"
        except:
            message = u"数据库错误"
        print message
        return render_template('scholarshipapply.html', message=message)
    return render_template('scholarshipapply.html', message="")

@app.route('/getscholarshipinfo/<username>', methods=['GET','POST'])
def getscholarshipinfo(username):
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    try:
        tmp = userdb.find_one({'username': username})
        if tmp['token'] != data['token']:
            result['message'] = u'请重新登录'
            return json.dumps(result)
        #result['info'] = 
        if tmp.has_key('scholarshipinfo'):
            result['scholarshipinfo'] = tmp['scholarshipinfo']
            result['success'] = 1
        print result
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)