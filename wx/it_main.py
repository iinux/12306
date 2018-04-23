# coding=utf8
import itchat
from flask import request, jsonify
import flask
import config

app = flask.Flask(__name__)
itchat.auto_login(hotReload=True)


@app.route("/wxpy", methods=['GET', 'POST'])
def index():
    key = request.args.get('key', 0, type=str)
    if key != config.key:
        return jsonify(result='key error')
    content = request.args.get('content', 0, type=unicode)
    
    who = request.args.get('who', type=unicode)
    if who is not None:
        wechat_send(who, content)
    else:
        wechat_send(u'张群', content)

    return jsonify(result='ok')


def wechat_send(who, content):
    f = itchat.search_friends(who)
    itchat.send(content, f[0]['UserName'])


# 进入Python命令行，让程序保持运行
# embed()
if __name__ == "__main__":
    app.run(host=config.flask_listen_host)
