import pymysql
# 打开数据库连接

def GetAll (db,cursor):
    cursor.execute("select * from result")
    alldata=cursor.fetchall()
    print(alldata)
# SQL 删除语句

def DelAll(db,cursor):
    # sql = "DELETE FROM datas WHERE age > '%d'" % (0)
    sql = "DELETE FROM result WHERE framecount >= '%d'" % (0)
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

db = pymysql.connect(host="106.14.206.16", user="pepe", password="qwertyuiop", database="pepeGame", charset='utf8',
                          use_unicode=True )
cursor = db.cursor()# 使用cursor()方法获取操作游标
GetAll(db,cursor)
# DelAll(db,cursor)
