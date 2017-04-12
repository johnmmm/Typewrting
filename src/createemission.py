# -*- coding=utf8 -*-
import os
import string
import codecs
import sqlite3

conn = sqlite3.connect('pinlist.sqlite')
print 'success'

if not os.path.exists('pinyinbiao/hanzibiao.txt'):
        print 'no'
else:
    f = codecs.open('pinyinbiao/hanzibiao1.txt', 'r', 'utf-8')
    s = f.read()
    arr = s.split("\n")
    total = 0;
    for strs in arr:
        if strs == "":
            #print 'kong'
            continue
        else:
            biao = strs.split(" ")
            pinyin = biao[0]
            #print len(biao)
            for tmp in biao:
                if tmp == pinyin:
                    continue
                total = total + 1
                if total%100 == 1:
                    print total
                        
                conn.execute("INSERT INTO EMISSION (ID,CHARACTER,PINYIN,PROBABILITY) \
                      VALUES (?, ?, ?, ?)", (total, tmp, pinyin, 0.0));
conn.commit()
