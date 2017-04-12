# -*- coding=utf8 -*-
import os
import string
import codecs
import sqlite3
import math

conn = sqlite3.connect('pinlist.sqlite')
print 'success'

pdict = {}
total=0.0

for i in range(1,6591):
    cursor = conn.cursor()
    cursor.execute('SELECT * from starting where id = ?',(i,))
    for item in cursor:
        pdict[item[1]]={}
        pdict[item[1]][0]=item[0]
        pdict[item[1]][1]=item[1]
        pdict[item[1]][2]=item[2]
        pdict[item[1]][3]=item[3]
        total=total+item[3]

ids = 6590.0
for a in range(2001,2017):
    for j in range(1,13):
        for m in range(1,32):
            for n in range(1,5):
                if not os.path.exists('stop.txt'):
                    #print ('no')
                    break;
                else:
                    f = codecs.open('stop.txt','r','utf-8')
                    s = f.read()
                    for chars in s:
                        flag = False
                        if pdict.has_key(chars):
                            times=pdict[chars][3]+1
                            total=total+1
                            pdict[chars][3] = times
                        else:
                            total=total+1
                            ids=ids+1
                            times=1
                            pdict[chars]={}
                            pdict[chars][0]=ids
                            pdict[chars][1]=chars
                            pdict[chars][2]=0.0
                            pdict[chars][3]=times
                            if total%100==1:
                                print total
for k in pdict:
    flags=False
    times=pdict[k][3]
    pdict[k][2]=math.log(times/total)
    cursor = conn.cursor()
    cursor.execute('SELECT * from starting where character = ?',(k,))
    for item in cursor:
        flags=True
        conn.execute("UPDATE starting set probability = ? where id = ?", (pdict[k][2],item[0]))
        conn.execute("UPDATE starting set frequency = ? where id = ?", (times,item[0]))
    if not flags:
        conn.execute("INSERT INTO STARTING (ID,CHARACTER,PROBABILITY,FREQUENCY) \
                    VALUES (?, ?, ?, ?)", (pdict[k][0], k, pdict[k][2], times))
print total
conn.commit()
                
            
            
            
        
