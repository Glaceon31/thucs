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
import string

userdb = db.user
logdb = db.log

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
            logdata = {}
            logdata['action'] = 'apply'
            logdata['scholarshipinfo'] = json.dumps(data)
            logdata['username'] = tmp['username']
            logdata['ip'] = request.remote_addr
            logdata['time'] = datetime.datetime.now()
            logdb.insert(logdata)
            userdb.update_one({'username':data['username']},{'$set':{'scholarshipinfo':json.dumps(data)}})
            message = u"提交成功"
        except:
            traceback.print_exc()
        #print message
        return render_template('scholarshipapply.html', message=message)
    return render_template('scholarshipapply.html', message="")

@app.route('/scholarshipcancel', methods=['GET','POST'])
def scholarshipcancel():
    jsondata = request.form
    data = immutabledict2dict(jsondata)
    result = {'success': 0}
    try:
        tmp = userdb.find_one({'username': data['username']})
        if tmp['token'] != data['token']:
            result['message'] = u'请重新登录'
            return json.dumps(result)
        logdata = {}
        logdata['action'] = 'cancel'
        logdata['username'] = tmp['username']
        logdata['ip'] = request.remote_addr
        logdata['time'] = datetime.datetime.now()
        logdb.insert(logdata)
        userdb.update_one({'username':data['username']},{'$unset':{'scholarshipinfo':1}})
        result['message'] = u'撤销成功'
        result['success']=1
        return json.dumps(result)
    except:
        traceback.print_exc()

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
        print len(result)
        return json.dumps(result)
    except:
        traceback.print_exc()

@app.route('/getscores/<username>', methods=['GET','POST'])
def getscores(username):
    scholarshipinfo = json.loads(getscholarshipinfo(username))['scholarshipinfo']
    scholarshipinfo = json.loads(scholarshipinfo)
    result = {}
    result['academic'] = getacademicscore(scholarshipinfo)[0]
    result['conf'] = getconferencescore(scholarshipinfo)[0]
    result['qikan'] = getqikanscore(scholarshipinfo)[0]
    result['patent'] = getpatentscore(scholarshipinfo)[0]
    result['project'] = getprojectscore(scholarshipinfo)[0]
    result['standard'] = getstanardscore(scholarshipinfo)[0]
    result['award'] = getawardscore(scholarshipinfo)[0]
    result['job'] = getjobscore(scholarshipinfo)[0]
    result['accupro'] = getaccuproscore(scholarshipinfo)[0]
    result['shegong'] = getshegongscore(scholarshipinfo)[0]
    #print result
    return json.dumps(result)

def getkeyinfo(scholarshipinfo):
    result = {}
    result['username'] = scholarshipinfo['username']
    result['name'] = scholarshipinfo['name']
    result['mentor'] = scholarshipinfo['mentor']
    result['A'],result['B'],result['C'],result['O'] = getpapernum(scholarshipinfo)
    result['patent'] = getpatentnum(scholarshipinfo)
    result['academic'], wrongtime1 = getacademicscore(scholarshipinfo)
    result['shegong'], wrongtime2 = getshegongscore(scholarshipinfo)
    #print result
    result['total'] = int(1000*(0.7*result['academic']+0.3*result['shegong']))/1000.0
    result['wrongtime'] = wrongtime1 or wrongtime2
    return result

def checktime(timestring, lastyear=''):
    try:
        if lastyear == u'是':
            last = True
        else:
            last = False
        times = timestring.split('/')
        if len(times) == 3:
            year,month,day = times
            year = string.atoi(year)
            month = string.atoi(month)
            day = string.atoi(day)
            if not last:
                if year == 2015 and month >= 9 and month <= 12:
                    return True
                if year == 2016 and month <= 8 and month >= 1:
                    return True
            if last:
                if year == 2015 and month >= 9 and month <= 12:
                    return True
                if year == 2016:
                    return True
                if year == 2017 and month <= 8 and month >= 1:
                    return True
            return False
        if len(times) == 2:
            year,month = times
            year = string.atoi(year)
            month = string.atoi(month)
            if not last:
                if year == 2015 and month >= 9 and month <= 12:
                    return True
                if year == 2016 and month <= 8 and month >= 1:
                    return True
            if last:
                if year == 2015 and month >= 9 and month <= 12:
                    return True
                if year == 2016:
                    return True
                if year == 2017 and month <= 8 and month >= 1:
                    return True
            return False
        return False
    except:
        return False

def getscholarshipscore(scholarshipinfo):
    return getacademicscore(scholarshipinfo)[0]+getshegongscore(scholarshipinfo)[0]

def getacademicscore(scholarshipinfo):
    confscore, wrongtime1 = getconferencescore(scholarshipinfo)
    qikanscore, wrongtime2 = getqikanscore(scholarshipinfo)
    patentscore, wrongtime3 = getpatentscore(scholarshipinfo)
    projectscore, wrongtime4 = getprojectscore(scholarshipinfo)
    standardscore, wrongtime5 = getstanardscore(scholarshipinfo)
    awardscore,wrongtime6 = getawardscore(scholarshipinfo)
    score = confscore+qikanscore+patentscore+projectscore+standardscore+awardscore
    wrongtime = wrongtime1 or wrongtime2 or wrongtime3 or wrongtime4 or wrongtime5 or wrongtime6
    return score, wrongtime

def getpapernum(scholarshipinfo):
    num = 0
    result = [0,0,0,0]
    score = {'A':0,'B':1,'C':2,'O':3}
    while scholarshipinfo.has_key('conf_author'+str(num)):
        if scholarshipinfo['conf_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['conf_time'+str(num)],scholarshipinfo['conf_lastyear'+str(num)]):
            num += 1
            continue
        level = scholarshipinfo['conf_CCF'+str(num)]
        if score.has_key(level):
            if scholarshipinfo.has_key('conf_yizuo'+str(num)):
                if scholarshipinfo['conf_yizuo'+str(num)] == u'是':
                    result[score[level]] += 1
        num += 1
    
    num = 0
    while scholarshipinfo.has_key('qikan_author'+str(num)):
        if scholarshipinfo['qikan_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['qikan_time'+str(num)],scholarshipinfo['qikan_lastyear'+str(num)]):
            num += 1
            continue
        level = scholarshipinfo['qikan_CCF'+str(num)]
        if score.has_key(level):
            if scholarshipinfo.has_key('qikan_yizuo'+str(num)):
                if scholarshipinfo['qikan_yizuo'+str(num)] == u'是':
                    result[score[level]] += 1
            else:
                result[score[level]] += 1
        num += 1
    return result

def getpatentnum(scholarshipinfo):
    result = 0
    num = 0
    while (scholarshipinfo.has_key('patent_author'+str(num))):
        if scholarshipinfo['patent_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['patent_time'+str(num)],scholarshipinfo['patent_lastyear'+str(num)]):
            num += 1
            continue
        result += 1
        num += 1
    return result


def getconferencescore(scholarshipinfo):
    num = 0
    result = 0
    wrongtime = False
    score = {'A full paper':5,'A short paper':3,'A poster':1,'A workshop':1,'A demo':1,
            'B full paper':3,'B short paper':1.5,'B poster':1,'B workshop':1,'B demo':1,
            'C full paper':1.5,'C short paper':1,'C poster':1,'C workshop':1,'C demo':1,
            'O full paper':1}
    while (scholarshipinfo.has_key('conf_author'+str(num))):
        if scholarshipinfo['conf_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['conf_time'+str(num)],scholarshipinfo['conf_lastyear'+str(num)]):
            num += 1
            wrongtime = True
            continue
        level_type = scholarshipinfo['conf_CCF'+str(num)]+' '+scholarshipinfo['conf_papertype'+str(num)]
        if scholarshipinfo.has_key('conf_yizuo'+str(num)):
            if scholarshipinfo['conf_yizuo'+str(num)] == u'是':
                if score.has_key(level_type):
                    result+= score[level_type]
        num += 1
    return result ,wrongtime

def getqikanscore(scholarshipinfo):
    num = 0
    result = 0
    wrongtime = False
    score = {'A full paper':5,'A short paper':3,'A poster':1,'A workshop':1,'A demo':1,
            'B full paper':3,'B short paper':1.5,'B poster':1,'B workshop':1,'B demo':1,
            'C full paper':1.5,'C short paper':1,'C poster':1,'C workshop':1,'C demo':1,
            'O full paper':1}
    while (scholarshipinfo.has_key('qikan_author'+str(num))):
        if scholarshipinfo['qikan_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['qikan_time'+str(num)],scholarshipinfo['qikan_lastyear'+str(num)]):
            num += 1
            wrongtime = True
            continue
        level = scholarshipinfo['qikan_CCF'+str(num)]+' '+scholarshipinfo['qikan_papertype'+str(num)]
        if score.has_key(level):
            if scholarshipinfo.has_key('qikan_yizuo'+str(num)):
                if scholarshipinfo['qikan_yizuo'+str(num)] == u'是':
                    result+= score[level]
            else:
                result+= score[level]
        num += 1
    return result,wrongtime

def getpatentscore(scholarshipinfo):
    result = 0
    num = 0
    wrongtime = False
    while (scholarshipinfo.has_key('patent_author'+str(num))):
        if scholarshipinfo['patent_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['patent_time'+str(num)],scholarshipinfo['patent_lastyear'+str(num)]):
            num += 1
            wrongtime = True
            continue
        if scholarshipinfo.has_key('patent_yizuo'+str(num)):
            if scholarshipinfo['patent_yizuo'+str(num)] == u'是':
                result += 1
        else:
            result += 1
        num += 1
    return min(1,result),wrongtime

def getprojectscore(scholarshipinfo):
    num = 0
    result = 0
    wrongtime = False
    score = {u'国家级奖励':3,u'省级部一等奖项目':2,u'省级部二等奖项目':1}
    while (scholarshipinfo.has_key('project_author'+str(num))):
        if scholarshipinfo['project_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['project_time'+str(num)],scholarshipinfo['project_lastyear'+str(num)]):
            num += 1
            wrongtime = True
            continue
        level = scholarshipinfo['project_type'+str(num)]
        if score.has_key(level):
            result+= score[level]
        num += 1
    return result,wrongtime

def getstanardscore(scholarshipinfo):
    result = 0
    num = 0
    wrongtime = False
    while (scholarshipinfo.has_key('standard_author'+str(num))):
        if scholarshipinfo['standard_author'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['standard_time'+str(num)],scholarshipinfo['standard_lastyear'+str(num)]):
            num += 1
            wrongtime = True
            continue
        num += 1
        result += 2
    return min(2,result),wrongtime

def getawardscore(scholarshipinfo):
    return 0, False

def getshegongscore(scholarshipinfo):
    jobscore, wrongtime1 = getjobscore(scholarshipinfo)
    accuproscore, wrongtime2 = getaccuproscore(scholarshipinfo)
    wrongtime = wrongtime1 or wrongtime2
    return min(10,jobscore+accuproscore), wrongtime

def getjobscore(scholarshipinfo):
    num = 0
    result = 0
    wrongtime = False
    score = {'A':5,'B':3,'C':0.5}
    while (scholarshipinfo.has_key('job_job'+str(num))):
        if scholarshipinfo['job_job'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['job_starttime'+str(num)]):
            num += 1
            wrongtime = True
            continue
        if not checktime(scholarshipinfo['job_endtime'+str(num)]):
            num += 1
            wrongtime = True
            continue
        level = scholarshipinfo['job_level'+str(num)]
        try:
            months = string.atoi(scholarshipinfo['job_months'+str(num)])
            months = min(12,months)
        except:
            months = 0
            print months
        if score.has_key(level):
            result+= int(1000*score[level]*months/12.0)/1000.0
        num += 1
    return result,wrongtime

def getaccuproscore(scholarshipinfo):
    num = 0
    result = 0
    wrongtime = False
    score = {'A':5,'B':4,'C':4,'D':3,'E':2,'F1':3,\
    'F2':2,'F3':1,'G':1,'H':1,'I':2,'J':1,'K1':1.5,'K2':1,'K3':0.5}
    while (scholarshipinfo.has_key('accupro_accupro'+str(num))):
        if scholarshipinfo['accupro_accupro'+str(num)] == "":
            num +=1
            continue
        if not checktime(scholarshipinfo['accupro_time'+str(num)]):
            num += 1
            wrongtime = True
            continue
        level = scholarshipinfo['accupro_accupro'+str(num)]
        if score.has_key(level):
            result+= score[level]
        num += 1
    return result,wrongtime