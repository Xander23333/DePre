import pandas as pd
import numpy as np
import pymysql
import sqlalchemy
from sqlalchemy import create_engine
import time
import json

def DelAll(db,cursor):
    sql = "DELETE FROM datas WHERE age > '%d'" % (0)
    # sql = "DELETE FROM result WHERE framecount >= '%d'" % (0)
    try:
       # 执行SQL语句
       cursor.execute(sql)
       # 提交修改
       db.commit()
       print("delete OK")
    except:
       # 发生错误时回滚
       db.rollback()
       print("delete error")
    # 关闭连接
    db.close()

 # 1. 用sqlalchemy构建数据库链接engine
connect_info = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format("pepe", "qwertyuiop", "106.14.206.16", "3306", "pepeGame")  #1
engine = create_engine(connect_info)

 # sql 命令
sql_cmd = "SELECT * FROM datas"
df = pd.read_sql(sql=sql_cmd, con=engine)
print('this is datas table')
print(df)

#气氛分界
DIS1=-20
DIS2=0

for frameCount in range(50):#record frame
    time.sleep(5)
    # 2. 用DBAPI构建数据库链接engine
    con = pymysql.connect(host="106.14.206.16", user="pepe", password="qwertyuiop", database="pepeGame", charset='utf8',
                          use_unicode=True)
    curr = con.cursor()
    df = pd.read_sql(sql_cmd, con)
    ave=[]
    fratim=[]
    if df.size>0:#if null，stop analysis
        others=df.iloc[:,4:12]#emotion
        smile=df.iloc[:,1]
        dfa=others.join(smile)
        score=np.average(dfa*100, axis=1,weights=[-10,-10,-20,0,10,0,-10,20,10])
        ave=np.average(score)
        print('the average score is',ave)#气氛评分
        print('this is NO.',frameCount)#帧序号
        #两个分界
        # funny bald rate: gender_3 age_4 bald_14
        BaldCal=df.iloc[:,2:4]
        BaldCal=BaldCal.join(df.iloc[:,14])
        age_E=30
        bald_E=0.3
        Programmer=BaldCal[(df['age']<=age_E)&(BaldCal['gender']=='male')&(df['bald']>=bald_E)]
        # print("get programmer:")
        # print(Programmer)
        Programmer_Portion=Programmer.iloc[:,0].size/BaldCal.iloc[:,0].size#有多少人
        # print("the portion is",Programmer_Portion*100,"%")

        if ave>DIS2:
            framedata=pd.DataFrame({'framecount':[frameCount],'score':[ave],'rank':['good'],'facenum':[df.size],'propro':[Programmer_Portion]})
        elif ave>DIS1:
            framedata=pd.DataFrame({'framecount':[frameCount],'score':[ave],'rank':['soso'],'facenum':[df.size],'propro':[Programmer_Portion]})
        else:
            framedata=pd.DataFrame({'framecount':[frameCount],'score':[ave],'rank':['alert'],'facenum':[df.size],'propro':[Programmer_Portion]})
        # print(framedata)
        pd.io.sql.to_sql(framedata,name='result', con=engine, if_exists='append')
        #3. 将DF 矩阵输出到sql
        DelAll(con,curr)
    else:
        print("no face in camera")

#FLASK输出流
#----------------------------event2:返回所有图的参数json，即整个result table-----------------