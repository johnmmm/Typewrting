# -*- coding=utf8 -*-
import os
import string
import codecs
from sqlalchemy import Column, String, Integer, Float, create_engine, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

current_dir = os.path.dirname(os.path.abspath(__file__))
db_name = os.path.join(current_dir, 'pinlist.sqlite')
engine = create_engine('sqlite:///{}'.format(db_name))

BaseModel = declarative_base()
HMMSession = sessionmaker(bind=engine)

class Starting(BaseModel):

    __tablename__ = 'starting'

    id = Column(Integer, primary_key=True)
    character = Column(String(1), nullable=False)
    probability = Column(Float, nullable=False)
    frequency = Column(Integer, nullable=False)
    

class Emission(BaseModel):
    '''拼音到字的转换'''
    __tablename__ = 'emission'

    id = Column(Integer, primary_key=True)
    character = Column(String(1), nullable=False)
    pinyin = Column(String(7), nullable=False)
    probability = Column(Float, nullable=False)

    @classmethod
    def add(cls, character, pinyin, probability):
        """
        Args:
            character (string): 汉字
            pinyin (string): 拼音
            probability (float): 概率
        """
        session = HMMSession()
        record = cls(character=character, pinyin=pinyin, probability=probability)
        session.add(record)
        session.commit()
        return record

class Transition(BaseModel):

    __tablename__ = 'transition'

    id = Column(Integer, primary_key=True)
    previous = Column(String(1), nullable=False)
    behind = Column(String(1), nullable=False)
    probability = Column(Float, nullable=False)
    frequency = Column(Integer, nullable=False)

def init_dp_tables():
    """
    创建表
    """
    if os.path.exists(db_name):
        os.remove(db_name)

    with open(db_name, 'w') as f:
        pass

    BaseModel.metadata.create_all(bind=engine, tables=[Transition.__table__,
                                                       Starting.__table__,
                                                       Emission.__table__])
    
'''
def init_starting():
    for i in range(1,12):
        if not os.path.exists('txt/'+'2016-'+str(i)+'.txt'):
            print 'no'
            break;
        else:
            f = codecs.open('txt/'+'2016-'+str(i)+'.txt', 'w', 'utf-8')
            s = f.read()
            arr = s.split("\n")
            for str in arr:
                if str == "":
                    print 'kong'
                    continue
                else:
                    break'''

def init_emission():
    emis = Emission()
    if not os.path.exists('pinyinbiao/hanzibiao.txt'):
        print 'no'
        return 0
    else:
        f = codecs.open('pinyinbiao/hanzibiao.txt')
        s = f.read()
        arr = s.split("\n")
        for str in arr:
            if str == "":
                print 'kong'
                continue
            else:
                biao = str.split(" ")
                for tmp in range(1, len(biao)):
                    print biao[tmp]
                    emis.add(biao[tmp], biao[0], 0)

if __name__ == '__main__':
    init_dp_tables()
    
    
