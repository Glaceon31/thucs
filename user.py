#-*- coding: utf-8 -*-
from flask import request
from app import app, db
import traceback
import json
import datetime
import random
from tools import *
import re

userdb = db.user

userinfolist = ['username', 'name']

def checkusername(username):
    if re.match('^[0-9a-zA-Z_]+$',username):
        return True
    else:
        return False

def checkemail(email):
    if re.match('^.+@.+$',email):
        return True
    else:
        return False

def checkmobile(mobile):
    if re.match('^[0-9]+$',mobile) and len(mobile) == 11:
        return True
    else:
        return False

def checknumber(number):
    if re.match('^[0-9]+$',number):
        return True
    else:
        return False

def checkidentity(identity):
    if re.match('^[0-9X]+$',identity) and (len(identity) == 15 or len(identity) == 18):
        return True
    else:
        return False

@app.route('/userregister', methods=['POST'])
def userregister():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success' :0}
    print data
    if len(data['username']) < 3:
        result['message'] = u'用户名过短'
        return json.dumps(result)
    for i in userinfolist:
        if data[i] == '':
            result['message'] = u'请填写所有项'
            return json.dumps(result)
    if not checknumber(data['username']):
        result['message'] = u'用户名只能包含字母、数字和下划线'
        return json.dumps(result)
    if data['code'] != 'thucs':
        result['message'] = u'邀请码错误'
        return json.dumps(result)
    #db
    try:
        #same username
        tmp = userdb.find_one({"username": data["username"]})
        if tmp:
            result['message'] = u'用户名已存在'
            return json.dumps(result)
        else:
            data['register_date'] = datetime.datetime.utcnow()
            data['applied'] = False
            data['applydate'] = ''
            data['lastmodify'] = ''
            '''
            if not savelog(data['username'], 'register', ''):
                result['message'] = u'后台错误'
                return json.dumps(result)
            '''
            user_id = userdb.insert_one(dict(data)).inserted_id
            result['success'] = 1
            result['message'] = u'注册成功'
            return json.dumps(result)
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)

@app.route('/userlogin', methods=['POST'])
def userlogin():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    #db
    try:
        tmp = userdb.find_one({"username": data["username"]})
        if not tmp:
            result['message'] = u'用户不存在'
            return json.dumps(result)
        else:
            if tmp['password'] == data['password']:
                tokenlength = random.randrange(16,32)
                token = ''
                for i in range(0, tokenlength):
                    token += random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
                result['success'] = 1
                result['userid'] = str(tmp['_id'])
                result['username'] = tmp['username']
                result['token'] = token
                userdb.update_one({'_id': tmp['_id']}, {'$set':{'token' : token}})
                return json.dumps(result)
            else:
                result['message'] = u'密码错误'
                return json.dumps(result)
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)

@app.route('/userchecklogin', methods=['POST'])
def userchecklogin():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] == data['token']:
            result['success'] = 1
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)
    #
    return '1'

@app.route('/usergetusername', methods=['POST'])
def usergetusername():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    try:
        tmp = userdb.find_one({'identity': data['identity']})
        if not tmp:
            result['message'] = u'用户不存在'
            return json.dumps(result)
        else:
            result['message'] = u'用户名: '+tmp['username']
            result['success'] = 1
            return json.dumps(result)
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)

@app.route('/getuserinfo', methods=['POST'])
def getuserinfo():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] != data['token']:
            result['message'] = u'请重新登录'
            return json.dumps(result)
        userinfolist = ['name','class','sex','school_roll','political','grade','suo'
                ,'ethnic','mas_doc','mentor','email', 'postcode','address','mobile']
        for i in userinfolist:
            if not tmp.has_key(i):
                tmp[i] = ''
            result[i] = tmp[i]
        '''
        for i in userinfolist_time:
            if not tmp.has_key(i):
                tmp[i] = ''
            if isinstance(tmp[i],datetime.datetime):
                tmp[i] += datetime.timedelta(hours=8) 
            result[i] = str(tmp[i])[0:19]
        '''

        result['success'] = 1
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)



@app.route('/userlogout', methods=['POST'])
def userlogout(jsondata):
    data = json.loads(jsondata)
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] == data['token']:
            if not savelog(data['username'], 'logout', data['token']):
                return u'后台错误'
            userdb.update_one({'username': data['username']}, {'$set':{'token' : ''}})
    except:
        traceback.print_exc()
        return '0'
    #
    return '1'

@app.route('/usergetinfo', methods=['POST'])
def getinfo(jsondata):
    data = json.loads(jsondata)
    result = {}
    try:
        a = 1
    except:
        print 'dberror'
        return 0
    #
    if data['token'] != token:
        return 0
    result = ''
    return result

@app.route('/usermodify', methods=['POST'])
def usermodify():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0 }
    if not checkemail(data['email']):
        result['message'] = u'邮箱格式不正确'
        return json.dumps(result)
    if not checkmobile(data['mobile']):
        result['message'] = u'手机号不正确'
        return json.dumps(result)
    if not checknumber(data['postcode']):
        result['message'] = u'邮编不正确'
        return json.dumps(result)
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
    except:
        traceback.print_exc()
        result['message'] = u'未知错误'
        return json.dumps(result)
    #
    if data['token'] != tmp['token']:
        result['message'] = u'登录已失效，请重新登录'
        return json.dumps(result)
    else:
        try:
            infolist = ['name','class','sex','school_roll','political','grade','suo'
                ,'ethnic','mas_doc','mentor','email', 'postcode','address','mobile']
            update = {}
            for info in infolist:
                update[info] = data[info]
            userdb.update_one({'username': data['username']}, 
                {'$set':update})
            '''
            {'email' : data['email'], 
                'postcode':data['postcode'],
                'mobile':data['mobile'],
                'address':data['address']}
            '''
        except:
            traceback.print_exc()
            result['message'] = u'后台错误'
            return json.dumps(result)
        result['message'] = u'修改成功'
        result['success'] = 1
        return json.dumps(result)

@app.route('/usermodifypassword', methods=['POST'])
def usermodifypassword():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success':0}
    #db
    try:
        tmp = userdb.find_one({'username': data['username']})
    except:
        traceback.print_exc()
        result['message'] = u'后台错误'
        return json.dumps(result)
    #
    if data['token'] != tmp['token']:
        result['message'] = u'登录已失效，请重新登录'
        return json.dumps(result)
    elif data['oldpassword'] != tmp['password']:
        result['message'] = u'原密码错误'
        return json.dumps(result)
    else:
        try:
            userdb.update_one({'username': data['username']}, {'$set':{'password' : data['newpassword']}})
        except:
            traceback.print_exc()
            result['message'] = u'后台错误'
            return json.dumps(result)
        result['success'] = 1
        result['message'] = u'修改密码成功'
        return json.dumps(result)