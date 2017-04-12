#-*-coding:utf-8-*-
import urllib
#import urllib2
import re
import os
import string
import codecs
import json
import sqlite3

conn = sqlite3.connect('pinlist.sqlite')
print 'success'

text = ''
'''
def replace(x):
    plist = []
    for i in range(1,7498):
        cursor = conn.cursor()
        cursor.execute('SELECT * from emission where id = ?', (i,))
        for item in cursor:
            #print item[1]
            plist.append(item[1])
    print 'success'
    for chars in x:
        
        if not chars in plist:
            x=x.replace(chars,"")
    return x
'''
def is_json(myjson):  
    try:  
        json.loads(myjson)  
    except ValueError:  
        return False  
    return True 


pdict = {}
for i in range(1,7498):
    cursor = conn.cursor()
    cursor.execute('SELECT * from emission where id = ?', (i,))
    for item in cursor:
        pdict[item[1]]=''
        pdict[item[1]]='T'
print 'success'
for i in range(10,11):
    if not os.path.exists('sina_news/'+'2016-'+str(i)+'.txt'):
        print ('no')
        break;
    else:
        f = codecs.open('sina_news/'+'2016-'+str(i)+'.txt','r','utf-8')
        s = f.read()
        arr = s.split("\n")
        print ('yes')
        print (len(arr))
        o = codecs.open('txt/'+'2016-'+str(i)+'.txt','w','utf-8')
        for l in range(0, len(arr)):
            if(is_json(arr[l])):
                jsona = json.loads(arr[l])
                text = jsona["html"]
                for chars in text:
                    if not pdict.has_key(chars):
                        text=text.replace(chars,"")
                        #text=text.lstrip(chars)
                o.write(text)
                if l%1000 == 0:
                    print l
                text = ''
        o.flush()
        print (str(i))
        text = ''
