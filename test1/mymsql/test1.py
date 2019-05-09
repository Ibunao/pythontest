from pymysql import *
import time


# 创建连接
conn = connect(host='127.0.0.1',port=3306,database='test',user='root',password='123456',charset='utf8')

cs = conn.cursor()

count = cs.execute('insert into test (content) values ("硬盘")')
count = cs.execute('insert into test (content) values ("光盘")')

time.sleep(300)
print('结束')
# 关闭Cursor对象
cs.close()
# 关闭Connection对象
conn.close()