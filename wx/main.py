# coding=utf8
from wxpy import *
from flask import request, jsonify
import flask
import config

app = flask.Flask(__name__)
bot = Bot(cache_path=True)
my_friend = bot.friends().search(u'张群', sex=MALE)[0]


@app.route("/", methods=['GET', 'POST'])
def index():
    key = request.args.get('key', 0, type=str)
    if key != config.key:
        return jsonify(result='key error')
    content = request.args.get('content', 0, type=str)
    my_friend.send(content)

    return jsonify(result='ok')


@bot.register()
def print_message(msg):
    print(msg.text)
    return msg.text


# bot.file_helper.send("hello")
# 发送文本给好友
# my_friend.send('Hello WeChat!')
# 发送图片
# my_friend.send_image('my_picture.jpg')

# 进入Python命令行，让程序保持运行
# embed()
if __name__ == "__main__":
    app.run(host=config.flask_listen_host)
