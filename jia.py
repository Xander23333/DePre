from flask import Flask
import time
from flask import make_response
import pandas as pd
import numpy as np
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import json

DIS1=2
dis2=3
# global framecount
framecount = 0
runflag=True
DF_history = pd.DataFrame(columns=['facenum', 'global framecount', 'propro', 'rank', 'score'])


#TODO untest
# def DFtoDict(out_df):
#     train_data = np.array(framedata)
#     train_x_list = train_data.tolist()[0]  # list
#     b_beta = train_x_list
#     b=[]
#     a = ['facenum', 'global framecount', 'propro', 'rank', 'score']
#     for i in train_x_list:
#         b.append(str(i))
#     print(train_x_list)#测试
#     data = pd.DataFrame(zip(a, b), columns=['project', 'attribute'])
#     print (data)#转置后的df
#     dict_country = data.set_index('project').T.to_dict('list')
#     print (dict_country)
#     return dict_country
#untest
def DicttoJson(out_dict):
    outt_dict={}
    for key in out_dict:
        llist=[]
        for value in (out_dict[key]).values():
            llist.append(value)
        outt_dict[key] = llist
    json_str = json.dumps(outt_dict)
    print("json_str =   {}  ".format(type(json_str)))#测试输出
    return json_str
 # 1. 用sqlalchemy构建数据库链接engine
connect_info = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format("pepe", "qwertyuiop", "localhost", "3306", "pepeGame")  #1
engine = create_engine(connect_info)

#----------------------------event1:实时返回单张图的json-----------------
 # sql 命令
sql_cmd = "SELECT * FROM data"
df = pd.read_sql(sql=sql_cmd, con=engine)
#print(df)

#气氛分界，待改

# while global runflag:#record frame，待改，改为事件发生时计数器加一

# time.sleep(2)
# 2. 用DBAPI构建数据库链接engine
con = pymysql.connect(host="localhost", user="pepe", password="qwertyuiop", database="pepeGame", charset='utf8', use_unicode=True)
cur=con.cursor()
df = pd.read_sql(sql_cmd, con)
ave=[]
fratim=[]
if df.columns.size>0:#if null，stop analysis

    # global framecount=framecount+1

    others=df.iloc[:,4:12]#emotion
    smile=df.iloc[:,1]
    dfa=others.join(smile)
    score=np.average(dfa*100, axis=1,weights=[-10,-10,-20,0,10,0,-10,20,10])
    ave=np.average(score)
    print(ave)
    print(type(ave))
    if ave>DIS1:
            framedata=pd.DataFrame({'global framecount':[framecount],'score':[ave],'rank':['good'],'facenum':[df.iloc[:,0].size],'propro':[Programmer_Portion]})
        elif ave>dis2:
            framedata=pd.DataFrame({'global framecount':[framecount],'score':[ave],'rank':['soso'],'facenum':[df.iloc[:,0].size],'propro':[Programmer_Portion]})
        else:
            framedata=pd.DataFrame({'global framecount':[framecount],'score':[ave],'rank':['alert'],'facenum':[df.iloc[:,0].size],'propro':[Programmer_Portion]})
