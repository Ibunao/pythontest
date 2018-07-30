# encoding=utf-8
import os
from pymysql import *
import re

conn = connect(host='localhost', port=3306, database='test1', user='root', password='123456', charset='utf8')
cs = conn.cursor()

count = cs.execute('select * from opera_singer')
data_list = cs.fetchall()  # 演唱者id

cs.execute('select * from opera')
opera_id_list = cs.fetchall()  # 戏曲id

for i in opera_id_list:
    opera_id = i[0]  # 戏曲id
    opera_name = i[5]  # 戏曲演唱者name
    singer_id = 1;
    for data in data_list:
        name_id = data[0]  # 演唱者id
        name = data[1]    # 演唱者name
        ret = re.findall(name,opera_name)
        print(ret)
        if ret:
            singer_id = name_id

    sql = "insert into opera_singer_relation(opera_id,singer_id) values ('%d','%d')" % (i[0], singer_id)
    try:
        print('ok')
        cs.execute(sql)
        conn.commit()
    except Exception as e:
        print(e)
    # break

# for i in opera_id_list:
#     singer_name = i[5]
#     for data in data_list:
#         name = data[1]
#
#         if re.findall(name, singer_name):
#             singer_id = data[0]
#         else:
#             singer_id = 1
#         print(singer_id)
#         sql = "insert into opera_singer_relation(opera_id,singer_id) values ('%d','%d')" % (i[0], singer_id)
#         try:
#             print('ok')
#             cs.execute(sql)
#             conn.commit()
#         except Exception as e:
#             print(e)
#     break
