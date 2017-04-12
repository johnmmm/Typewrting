# -*- coding=utf8 -*-
import os
import string
import codecs
import sqlite3
import math

conn = sqlite3.connect('pinlist.sqlite')
print 'success'

pdict = {}
total = 0.0
ids = 4230634

for i in range(1,4230635):
    cursor = conn.cursor()
    cursor.execute('SELECT * from transition where id = ?',(i,))
    for item in cursor:
        if pdict.has_key(item[1]):
            pdict[item[1]][item[2]]={}
            pdict[item[1]][item[2]][0]=item[0]
            pdict[item[1]][item[2]][1]=item[1]
            pdict[item[1]][item[2]][2]=item[2]
            pdict[item[1]][item[2]][3]=item[3]
            pdict[item[1]][item[2]][4]=item[4]
            total=total+item[4]
        else:
            pdict[item[1]]={}
            pdict[item[1]][item[2]]={}
            pdict[item[1]][item[2]][0]=item[0]
            pdict[item[1]][item[2]][1]=item[1]
            pdict[item[1]][item[2]][2]=item[2]
            pdict[item[1]][item[2]][3]=item[3]
            pdict[item[1]][item[2]][4]=item[4]
            total=total+item[4]
print 'success'

for a in range(2001,2002):
    for j in range(1,2):
        print j
        for m in range(1,2):
            for n in range(1,5000):
                if not os.path.exists('stop.txt'):
                    #print ('no')
                    continue;
                else:
                    f = codecs.open('stop.txt','r','utf-8')
                    #f = codecs.open('stop.txt','r','utf-8')
                    s = f.read()
                    #print len(s)
                    for i in range(0,len(s)):
                        flag = False
                        if i == len(s)-1:
                            break
                        if pdict.has_key(s[i]):
                            if pdict[s[i]].has_key(s[i+1]):
                                times=pdict[s[i]][s[i+1]][4]+1
                                pdict[s[i]][s[i+1]][4]=times
                                total=total+1
                                flag=True
                        if not flag:
                            total=total+1
                            ids=ids+1
                            times=1
                            if pdict.has_key(s[i]):
                                if pdict[s[i]].has_key(s[i+1]):
                                    print 'miaomiaomiao?'
                                else:
                                    pdict[s[i]][s[i+1]]={}
                                    pdict[s[i]][s[i+1]][0]=ids
                                    pdict[s[i]][s[i+1]][1]=s[i]
                                    pdict[s[i]][s[i+1]][2]=s[i+1]
                                    pdict[s[i]][s[i+1]][3]=0.0
                                    pdict[s[i]][s[i+1]][4]=times
                            else:
                                pdict[s[i]]={}
                                pdict[s[i]][s[i+1]]={}
                                pdict[s[i]][s[i+1]][0]=ids
                                pdict[s[i]][s[i+1]][1]=s[i]
                                pdict[s[i]][s[i+1]][2]=s[i+1]
                                pdict[s[i]][s[i+1]][3]=0.0
                                pdict[s[i]][s[i+1]][4]=times
                            if total%10000==0:
                                print total
for k1 in pdict:
    for k2 in pdict[k1]:
        flags=False
        #print pdict[k1][k2][1]+pdict[k1][k2][2]
        #print pdict[k1][k2][0]
        times=pdict[k1][k2][4]
        pdict[k1][k2][3]=math.log(times/total)
        cursor = conn.cursor()
        cursor.execute('SELECT * from transition where id = ?',(pdict[k1][k2][0],))
        for item1 in cursor:
            cursors = conn.cursor()
            cursors.execute('SELECT * from transition where id = ?',(item1[0],))
            for item2 in cursors:
                flags = True
                conn.execute("UPDATE transition set probability = ? where id = ?", (pdict[k1][k2][3],item2[0]))
                conn.execute("UPDATE transition set frequency = ? where id = ?", (times,item2[0]))
        if not flags:
            conn.execute("INSERT INTO transition (ID,previous,BEHIND,PROBABILITY,FREQUENCY) \
                        VALUES (?, ?, ?, ?, ?)",(pdict[k1][k2][0],k1,k2,pdict[k1][k2][3],times))
print total
conn.commit()
                
        

