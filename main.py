# import---------------
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

# address---------------
img_url = 'picture.jpg'  # prefer .jpg to .jpeg! :P
# fileAddress="command.txt"
table = "datas"

# const---------------------
requests.packages.urllib3.disable_warnings()

# faceAPI

# KEY = 'cd3dd0d37ea24072bf46ebb12f648952'  # KEY for hackathon, might be expired yet
# CF.Key.set(KEY)
# BASE_URL = 'https://api.cognitive.azure.cn/face/v1.0'   # bound with KEY
# CF.BaseUrl.set(BASE_URL)

KEY = '3f476c6650914d70abece1702871b6d6'  # my KEY for trying, expire in 5/14/2018    ......add by Richard
CF.Key.set(KEY)
BASE_URL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0'  # bound with KEY
CF.BaseUrl.set(BASE_URL)

# MySQL
db = pymysql.connect(host="106.14.206.16", user="pepe", password="qwertyuiop", db="pepeGame", charset='utf8')
cur = db.cursor()

# camera
cap = cv2.VideoCapture(0)
cap.set(3, 1920)
cap.set(4, 1080)


# variables

# execute------------------
def record():
    print("camera start......")
    global flag
    global frame
    flag = False
    ret, frame = cap.read()

    tc.setDaemon(True)
    tc.start()

    while (1):
        ret, frame = cap.read()
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    flag = True
    print("camera exit......success")


def FaceToCommand():
    faces = CF.face.detect(img_url, landmarks=False, attributes='age,gender,hair,smile,emotion,makeup')
    print("\nthe number of recognized faces is {}\n".format(len(faces)))

    # f1=open(fileAddress,"w")
    dicts = []
    for dict in faces:
        dict2 = {}

        dict2['faceId'] = '\"' + dict['faceId'] + '\"'

        dictt1 = dict['faceAttributes']
        dict2['smile'] = dictt1['smile']
        dict2['gender'] = '\"' + dictt1['gender'] + '\"'
        dict2['age'] = dictt1['age']

        dictt2 = dictt1['emotion']
        for key in dictt2:
            dict2[key] = dictt2[key]

        dictt3 = dictt1['makeup']
        for key in dictt3:
            dict2[key] = dictt3[key]

        dict2['bald'] = dictt1['hair']['bald']
        # print(dict2)
        dicts.append(dict2)
    # output a dicts component of dict2 which just has one layer

    #  f=open(fileAddress,"w")

    for dict2 in dicts:
        namestr = ",".join(dict2.keys())

        valuestr = []
        tmp = dict2.values()
        for i in tmp:
            valuestr.append(str(i))
        valuestr = ",".join(valuestr)

        SQL_insert = "insert into {}({}) values({})".format(table, namestr, valuestr)

        try:
            cur.execute(SQL_insert)
            # commit
            db.commit()
        except Exception as e:
            # rollback
            print("write to DB......error")
            db.rollback()
        finally:
            print("write to DB......success")

        # try:
        #     print(sql_insert,file = f1)
        # except Exception as e:
        #     print("error2")
        # finally:
        #     print("success2")

    # f1.close()


# def FreshSQL():   # No use now
#     f2=open(fileAddress,"r")
#
#     for line in f2:
#         line=line.strip('\n')
#         try:
#             cur.execute(SQL_insert)
#             #提交
#             db.commit()
#         except Exception as e:
#             #错误回滚
#             print("error3")
#             db.rollback()
#         finally:
#             print("success3")
#
#     f2.close()

def cam():
    print("core start......")
    while (1):
        cv2.imwrite(img_url, frame)

        # face To Command
        FaceToCommand()

        # fresh SQL
        # FreshSQL()

        if flag:
            break
        time.sleep(5)
    # close
    cur.close()
    db.close()
    cap.release()
    cv2.destroyAllWindows()

    print("core exit......success")


# main Func
print("program start...")

tr = threading.Thread(target=record, args=())
tc = threading.Thread(target=cam, args=())
tr.start()

print("end of Program...")
