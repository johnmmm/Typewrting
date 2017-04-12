# -*- coding=utf8 -*-
import os
import sys
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
                dicttr[chars]=math.log(pdictt[character][chars]/float(pdicts[character]))+pdicte[pinyin][chars]
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
                num=num+1
                if num > 5:
                    break
                character = phrase[-1]
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

def cur_file_dir():
     path = sys.path[0]
     if os.path.isdir(path):
         return path
     elif os.path.isfile(path):
         return os.path.dirname(path)

if __name__ == '__main__':
    if getattr(sys, 'frozen', False):
        application_path = os.path.dirname(sys.executable)
    elif __file__:
        application_path = os.path.dirname(__file__)

    print application_path

    conn = sqlite3.connect(application_path+'/pinlist.sqlite')
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
    for i in range(1,6591):
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
    
    while 1:
        print '请选择你想要进行的模式，进行文件分析请输入1，直接进行翻译请按2'
        modelnum = raw_input('你选择的模式是：')
        if modelnum == '1':
            input_place = raw_input('请输入你要翻译的文件的地址:')
            if not os.path.exists(input_place):
                print 'Can not find the file!!'
                continue
            else:
                out_place = raw_input('请输入你的文件要输出的地址:')
                if not os.path.exists(out_place):
                    print 'Can out find the path!!'
                    continue
                else:
                    fin = codecs.open(input_place,'r','utf-8')
                    s = fin.read()
                    fout = codecs.open(out_place+'/output.txt','w','utf-8')
                    arr = s.split('\n')
                    for lines in range(0, len(arr)):
                        string = arr[lines]
                        string = string.lower()
                        pinyin_list = string.split()
                        V = viterbi(pinyin_list)
                        for phrase, prob in sorted(V.items(), key=lambda d:d[1], reverse=True):
                            fout.write(phrase+'\n')
                            fout.write(str(prob)+'\n')
                            print lines
                            break
                    fin.close()
                    fout.close()
        elif modelnum == '2':
            while 1:
                string = raw_input('Please input:')
                if string == 'exit':
                    break
                string = string.lower()
                pinyin_list = string.split()
                V = viterbi(pinyin_list)
                for phrase, prob in sorted(V.items(), key=lambda d: d[1], reverse=True):
                    print phrase
                    print prob
        elif modelnum == '2333':
            break2333
        else:
            print 'Come on! Stop making too much fun!'
            continue
            
            
            
