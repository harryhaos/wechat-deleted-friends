#coding=utf-8

import os
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash
from sl2 import check_user_delete,get_user_qr

app = Flask(__name__)

app.config.update(dict(
    DEBUG=True,
    SECRET_KEY='5jdlxzpgfd40alho82tcdkyabl',
))

#-----------------------------------------------------------------

def blank_page():
    return render_template('index.html' )


@app.route('/')
def index():
    reminder_ = u"扫描登陆以查看被删除好友，结果可能引起不适，请慎重"
    qrpath = os.path.basename(get_user_qr())
    session['qr_path'] = qrpath

    return render_template('show_qr.html',qr_img= qrpath,reminder_=reminder_)

@app.route('/delete_result')
def delete_result():
    flash(u'请不要在群聊中发言,请稍后')
    qrpath = 'static/' + session.get('qr_path')
    if qrpath is None:
        return "login fail"
    result = check_user_delete(qrpath)
    if result is None:
        return "No data or no users detele you"
    result.insert(0, u'以下好友删除了你：')
    return unicode("\n".join(result), "utf-8")




if __name__ == '__main__':
    app.run(debug=True)
