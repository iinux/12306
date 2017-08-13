#!/usr/bin/python
# -*- coding: UTF-8 -*-

import flask
from flask import request
import MySQLdb
import config

app = flask.Flask(__name__)

db = MySQLdb.connect(config.mysql_host, config.mysql_user, config.mysql_password, config.mysql_database)
db.set_character_set('utf8')

# 使用cursor()方法获取操作游标
cursor = db.cursor()


@app.route("/")
def index():
    query_update_at = request.args.get('update_at')

    cursor.execute("select distinct(update_at) from bj_metro_real_data order by update_at desc")
    # 使用 fetchone() 方法获取一条数据库。
    all_update_at = cursor.fetchall()
    newest_time = all_update_at[0][0].strftime('%Y-%m-%d %H:%M')

    return_string = ""
    return_string += newest_time + "<br />"

    if query_update_at:
        cursor.execute("select * from bj_metro_real_data where update_at=%s", query_update_at)
    else:
        cursor.execute("select * from bj_metro_real_data where update_at=%s", newest_time)
    data = cursor.fetchall()
    for row in data:
        row_string = "%s %s %s %s" % (row[5], row[6], row[4].strftime("%Y-%m-%d %H:%M"), row[3])
        return_string += row_string + "<br />"

    for update_at in all_update_at:
        update_at = update_at[0].strftime('%Y-%m-%d %H:%M')
        return_string += """<a href='/?update_at=%s'>%s</a><br />""" % (update_at, update_at)

    return return_string


if __name__ == "__main__":
    app.run(host=config.flask_listen_host)
