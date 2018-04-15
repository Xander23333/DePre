#address---------------
img_url = 'test.jpeg'
fileaddress="command.txt"
table="data"

#import---------------
import cv2
import time

import cognitive_face as CF
import urllib3
import requests

import threading

import pymysql

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy import create_engine


#const---------------------
requests.packages.urllib3.disable_warnings()

#faceAPI
KEY = 'cd3dd0d37ea24072bf46ebb12f648952'
CF.Key.set(KEY)
BASE_URL = 'https://api.cognitive.azure.cn/face/v1.0'
CF.BaseUrl.set(BASE_URL)

#mysql
db = pymysql.connect(host="localhost",user="pepe",password="qwertyuiop",db="pepeGame",charset='utf8')
cur = db.cursor()  

# SQLtodf
# connect_info = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format("pepe", "qwertyuiop", "localhost", "3306", "pepeGame")  #1
# engine = create_engine(connect_info)

#camera
cap = cv2.VideoCapture(0)
cap.set(3,1920)
cap.set(4,1080)
# cap.set(1,10.0)

#execute------------------
def record():
    global flag
    global frame
    flag=False
    retx,frame = cap.read()

    tc.setDaemon(True)
    tc.start()

    while(1):
        ret,frame = cap.read()
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    flag=True

def FaceToCommand():
    faces = CF.face.detect(img_url,landmarks=False,attributes='age,gender,hair,smile,emotion,makeup')
    print("\nthe number of recognized faces is {}\n".format(len(faces)))

    f1=open("command.txt","w")
    dicts=[]
    for dict in faces:
        dict2={}
        
        dict2['faceId']='\"'+dict['faceId']+'\"'

        dictt1=dict['faceAttributes']
        dict2['smile']=dictt1['smile']
        dict2['gender']='\"'+dictt1['gender']+'\"'
        dict2['age']=dictt1['age']

        dictt2=dictt1['emotion']
        for key in dictt2:
            dict2[key]=dictt2[key]

        dictt3=dictt1['makeup']
        for key in dictt3:
            dict2[key]=dictt3[key]
        
        dict2['bald']=dictt1['hair']['bald']
    # print(dict2)
        dicts.append(dict2)
    # output a dicts component of dict2 which just has one layer

    #  f=open(fileaddress,"w")
    
    for dict2 in dicts:
        namestr=",".join(dict2.keys())
        
        valuestr=[]
        tmp=dict2.values()
        for i in tmp:
            valuestr.append(str(i))
        valuestr=",".join(valuestr)

        sql_insert="insert into {}({}) values({})".format(table,namestr,valuestr)
        
        try:
            print(sql_insert)  
        except Exception as e:
            print("error2")
        finally: 
            print("success2")

    f1.close()

def FreshSQL():
    f2=open("command.txt","r")

    for line in f2:
        line=line.strip('\n')
        try:  
            cur.execute(line)
            #提交  
            db.commit()  
        except Exception as e:  
            #错误回滚  
            print("error3")
            db.rollback()
        finally: 
            print("success3")

    f2.close()

# def SQLtoDF():    
#     sql_cmd = "SELECT * FROM datas"
#     df = pd.read_sql(sql=sql_cmd, con=engine)
#     print(df)
#     DIS1=2
#     DIS2=3
#     for frameCount in range(3):#record frame
#         # 2. 用DBAPI构建数据库链接engine
#         df = pd.read_sql(sql_cmd, db)
#         ave=[]
#         fratim=[]
#         if df.columns.size>0:#if null，stop analysis
#             others=df.iloc[:,4:12]#emotion
#             smile=df.iloc[:,1]
#             dfa=others.join(smile)
#             score=np.average(dfa*100, axis=1,weights=[-10,-10,-20,0,10,0,-10,20,10])
#             ave=np.average(score)
#             print(ave)#气氛评分
#             print(frameCount)#帧序号
#             #两个分界
            
#             if ave>DIS1:
#                 framedata=pd.DataFrame({'score':[ave],'rank':['good'],'count':[frameCount]})
#             elif ave>DIS2:
#                 framedata=pd.DataFrame({'score':[ave],'rank':['soso'],'count':[frameCount]})
#             else:
#                 framedata=pd.DataFrame({'score':[ave],'rank':['alert'],'count':[frameCount]})
#             print(framedata)
#             pd.io.sql.to_sql(framedata,'result', engine, schema='pepeGame', if_exists='append') 

def cam():
    while(1):

        cv2.imwrite(img_url, frame)

        #faces = CF.face.detect(img_url,landmarks=False,attributes='age,gender,hair,smile,emotion,makeup')

        # facetocommand
        FaceToCommand()
        # freshsql
        FreshSQL()

        if flag:
            break

        time.sleep(5)
   
    cur.close()
    db.close()
    cap.release()
    cv2.destroyAllWindows()


tr = threading.Thread(target=record,args=())
tc = threading.Thread(target=cam,args=())
tr.start()
