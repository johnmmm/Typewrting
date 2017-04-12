# -*- coding=utf8 -*-
import os
import string
import codecs
import sqlite3
import math
import datetime

def starting(pinyin, limit=5):
    result=[]
    dictem={}
    if not pdicte.has_key(pinyin):
        return result
    for chars in pdicte.get(pinyin):
        if pdicts.has_key(chars):
            dictem[chars]=math.log(pdicts[chars]/592598360.0)+pdicte[pinyin][chars]
    num=0
    for chars, pro in sorted(dictem.items(), key=lambda d:d[1], reverse=True):
        num=num+1
        if(num > limit):
            break;
        result.append((chars,pro))
    return result

def transition(pinyin, character, limit=5):
    result=[]
    dictem={}
    dicttr={}
    flag=False
    if not pdicte.has_key(pinyin):
        return result
    for chars in pdicte.get(pinyin):
        if pdicts.has_key(chars):
            dictem[chars]=pdicts[chars]
    if pdictt.has_key(character):
        for chars in pdictt[character]:
            if dictem.has_key(chars):
                dicttr[chars]=math.log(pdictt[character][chars]/float(pdicts[character]))+pdicte[pinyin][chars])
                flag=True
            else:
                continue
    else:
        return starting(pinyin)
    
    if not flag:
        return starting(pinyin)
    
    num=0
    for chars, pro in sorted(dicttr.items(), key=lambda d:d[1], reverse=True):
        num=num+1
        if(num > limit):
            break;
        result.append((chars,pro))
    return result

def viterbi(pinyin_list):
    start_char = starting(pinyin_list[0])
    V = {char: prob for char, prob in start_char}
    tmp = 0
    while 1:
        for i in range(tmp+1, len(pinyin_list)):
            if i >= len(pinyin_list):
                break
            pinyin = pinyin_list[i]
            prob_map = {}
            num = 0
            for phrase, prob in sorted(V.items(), key=lambda d:d[1], reverse=True):
                #print phrase
                #print prob
                num=num+1
                if num > 5:
                    break
                character = phrase[-1]
                #new one:
                result = transition(pinyin, character)
                if not result:
                    continue
                for results in result:
                    state, new_prob = results
                    prob_map[phrase + state] = new_prob + prob
            tmp = tmp + 1
            if prob_map:
                V = prob_map
            else:
                break;
        if tmp+1 >= len(pinyin_list):
            return V

if __name__ == '__main__':
    conn = sqlite3.connect('pinlist.sqlite')
    print 'success'

    pdicte = {}
    for i in range(1,7498):
        cursor = conn.cursor()
        cursor.execute('SELECT * from emission where id = ?', (i,))
        for item in cursor:
            if pdicte.has_key(item[2]):
                pdicte[item[2]][item[1]]=item[3]
            else:
                pdicte[item[2]]={}
                pdicte[item[2]][item[1]]=item[3]
    print 'success emission'

    pdicts = {}
    for i in range(1,6588):
        cursor = conn.cursor()
        cursor.execute('SELECT * from starting where id = ?',(i,))
        for item in cursor:
            pdicts[item[1]]=0.0
            pdicts[item[1]]=item[3]
    print 'success starting'

    pdictt = {}
    for i in range(1,4230635):
        cursor = conn.cursor()
        cursor.execute('SELECT * from transition where id = ?',(i,))
        for item in cursor:
            if pdictt.has_key(item[1]):
                pdictt[item[1]][item[2]]=item[4]
            else:            
                pdictt[item[1]]={}
                pdictt[item[1]][item[2]]=item[4]
    print 'success transition'
    
    input_file = raw_input('input:')
    if not os.path.exists(input_file):
        print 'no'
    else:
        f = codecs.open(input_file,'r','utf-8')
        s = f.read()
        arr = s.split('\n')
        total_words = 0.0
        total_sen = 0.0
        words = 0.0
        sen = 0.0
        begin=datetime.datetime.now()
        for lines in range(0, len(arr)):
            if lines % 2 == 1:
                continue
            string = arr[lines]
            string = string.lower()
            pinyin_list = string.split()
            V = viterbi(pinyin_list)
            for phrase, prob in sorted(V.items(), key=lambda d:d[1], reverse=True):
                out_sen=phrase
                print phrase
                break
            place=lines+1
            answer = arr[place]
            flag = True
            corr_num = 0
            for charnum in range(0, len(answer)):
                if charnum+1 > len(out_sen):
                    flag=False
                    break
                else:
                    if answer[charnum]==out_sen[charnum]:
                        corr_num=corr_num+1
                    else:
                        flag=False
            if flag:
               sen=sen+1
            words=words+corr_num
            total_sen=total_sen+1
            total_words=total_words+len(answer)
            print sen
            print total_sen
            print words
            print total_words
            print '句子正确率:'+str(sen/total_sen)
            print '单字正确率:'+str(words/total_words)
            end=datetime.datetime.now()
            print end-begin
