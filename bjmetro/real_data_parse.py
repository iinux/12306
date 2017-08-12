#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from sys import argv
import MySQLdb
import beijing_parse

# 打开数据库连接
db = MySQLdb.connect("localhost", "root", "", "bjmetro")
db.set_character_set('utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()

argv_len = argv.__len__()
i = 1

beijing_parse = beijing_parse.Parse()

while i < argv_len:
    filename = argv[i]
    i += 1
    file_description = open(filename)
    content = file_description.read()

    print ("process %s" % filename)

    decode_json = json.loads(content)
    for seg in decode_json:
        from_name = beijing_parse.acc_name_map[seg['fs']]
        to_name = beijing_parse.acc_name_map[seg['ts']]
        print from_name, to_name, seg['color'], seg['update_at']
        # 使用execute方法执行SQL语句
        cursor.execute("SELECT * from bj_metro_real_data where fs=%s and ts=%s and update_at=%s",
                       (seg['fs'], seg['ts'], seg['update_at']))

        # 使用 fetchone() 方法获取一条数据库。
        data = cursor.fetchone()
        if data is None:
            try:
                # 执行sql语句
                cursor.execute(
                    """INSERT INTO bj_metro_real_data(id,fs,ts,color,update_at,from_name,to_name) VALUES (%s,%s,%s,%s,%s,%s,%s)""",
                    (seg['id'], seg['fs'], seg['ts'], seg['color'], seg['update_at'], from_name, to_name))
                # 提交到数据库执行
                db.commit()
            except Exception, e:
                print(e)
                # 发生错误时回滚
                db.rollback()

# 关闭数据库连接
db.close()
