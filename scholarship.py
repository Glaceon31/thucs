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
            #print data
            tmp = userdb.find_one({'username': data['username']})
            if tmp['token'] != data['token']:
                message = u'请重新登录'
                assert 0 == 1
            userdb.update_one({'username':data['username']},{'$set':{'scholarshipinfo':json.dumps(data)}})
            message = u"提交成功"
        except:
            traceback.print_exc()
        print message
        return render_template('scholarshipapply.html', message=message)
    return render_template('scholarshipapply.html', message="")

@app.route('/getscholarshipinfo/<username>', methods=['GET','POST'])
def getscholarshipinfo(username):
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    #print data
    result = {'success': 0}
    try:
        tmp = userdb.find_one({'username': username})
        '''
        if tmp['token'] != data['token']:
            result['message'] = u'请重新登录'
            return json.dumps(result)
        '''
        #result['info'] = 
        if tmp.has_key('scholarshipinfo'):
            result['scholarshipinfo'] = tmp['scholarshipinfo']
            result['success'] = 1
        #print result
        return json.dumps(result)
    except:
        traceback.print_exc()
        return json.dumps(result)

@app.route('/getscholarshiplist', methods=['GET','POST'])
def getscholarshiplist():
    try:
        tmp = userdb.find()
        a = [entry for entry in tmp]
        print len(a)
        result = []
        for tmpuser in a:
            if tmpuser.has_key('scholarshipinfo'):
                scholarshipinfo = json.loads(tmpuser['scholarshipinfo'])
                tmpresult = getkeyinfo(scholarshipinfo)

                result.append(tmpresult)
                result = sorted(result, key=lambda x:x['academic'],reverse=True)
        return json.dumps(result)
    except:
        traceback.print_exc()

@app.route('/getscores/<username>', methods=['GET','POST'])
def getscores(username):
    scholarshipinfo = json.loads(getscholarshipinfo(username))['scholarshipinfo']
    scholarshipinfo = json.loads(scholarshipinfo)
    result = {}
    result['conf'] = getconferencescore(scholarshipinfo)
    result['qikan'] = getqikanscore(scholarshipinfo)
    result['patent'] = getpatentscore(scholarshipinfo)
    result['job'] = getjobscore(scholarshipinfo)
    print result
    return json.dumps(result)

def getkeyinfo(scholarshipinfo):
    result = {}
    result['username'] = scholarshipinfo['username']
    result['name'] = scholarshipinfo['name']
    result['mentor'] = scholarshipinfo['mentor']
    result['A'],result['B'],result['C'],result['O'] = getpapernum(scholarshipinfo)
    result['patent'] = getpatentnum(scholarshipinfo)
    result['academic'] = getacademicscore(scholarshipinfo)
    result['shegong'] = getshegongscore(scholarshipinfo)
    print result
    result['total'] = int(10*(0.7*result['academic']+0.3*result['shegong']))/10.0
    return result

def getscholarshipscore(scholarshipinfo):
    return getacademicscore(scholarshipinfo)+getshegongscore(scholarshipinfo)

def getacademicscore(scholarshipinfo):
    return getconferencescore(scholarshipinfo)+\
            getqikanscore(scholarshipinfo)+\
            getpatentscore(scholarshipinfo)+\
            getprojectscore(scholarshipinfo)+\
            getstanardscore(scholarshipinfo)+\
            getawardscore(scholarshipinfo)

def getpapernum(scholarshipinfo):
    num = 0
    result = [0,0,0,0]
    score = {'A':0,'B':1,'C':2,'O':3}
    while scholarshipinfo.has_key('conf_author'+str(num)):
        level = scholarshipinfo['conf_CCF'+str(num)]
        if score.has_key(level):
            result[score[level]] += 1
        num += 1
    
    num = 0
    while scholarshipinfo.has_key('qikan_author'+str(num)):
        level = scholarshipinfo['qikan_CCF'+str(num)]
        if score.has_key(level):
            result[score[level]] += 1
        num += 1
    return result

def getpatentnum(scholarshipinfo):
    num = 0
    while (scholarshipinfo.has_key('patent_author'+str(num))):
        num += 1
    return num


def getconferencescore(scholarshipinfo):
    num = 0
    result = 0
    score = {'A':5,'B':3,'C':1.5,'O':0.5}
    while (scholarshipinfo.has_key('conf_author'+str(num))):
        level = scholarshipinfo['conf_CCF'+str(num)]
        if score.has_key(level):
            result+= score[level]
        num += 1
    return result

def getqikanscore(scholarshipinfo):
    num = 0
    result = 0
    score = {'A':5,'B':3,'C':1.5,'O':0.5}
    while (scholarshipinfo.has_key('qikan_author'+str(num))):
        level = scholarshipinfo['qikan_CCF'+str(num)]
        if score.has_key(level):
            result+= score[level]
        num += 1
    return result

def getpatentscore(scholarshipinfo):
    num = 0
    while (scholarshipinfo.has_key('patent_author'+str(num))):
        num += 1
    return min(1,num)

def getprojectscore(scholarshipinfo):
    return 0

def getstanardscore(scholarshipinfo):
    return 0

def getawardscore(scholarshipinfo):
    return 0

def getshegongscore(scholarshipinfo):
    return getjobscore(scholarshipinfo)+getaccuproscore(scholarshipinfo)

def getjobscore(scholarshipinfo):
    num = 0
    result = 0
    score = {'A':5,'B':3,'C':0.5}
    while (scholarshipinfo.has_key('job_job'+str(num))):
        level = scholarshipinfo['job_level'+str(num)]
        if score.has_key(level):
            result+= score[level]
        num += 1
    return min(10, result)

def getaccuproscore(scholarshipinfo):
    num = 0
    result = 0
    score = {'A':5,'B':4,'C':4,'D':3,'E':2}
    while (scholarshipinfo.has_key('accupro_accupro'+str(num))):
        level = scholarshipinfo['accupro_accupro'+str(num)]
        if score.has_key(level):
            result+= score[level]
        num += 1
    return 0