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

if __name__ == "__main__":
    tmp = userdb.find()
    a = [entry for entry in tmp]
    print len(a)
    result = {}
    for tmpuser in a:
        if tmpuser.has_key('scholarshipinfo'):
            scholarshipinfo = json.loads(tmpuser['scholarshipinfo'])
            suo = scholarshipinfo['suo']
            if result.has_key(suo):
                result[suo] += 1
            else:
                result[suo] = 1
    for key in result:
        print key, result[key]
