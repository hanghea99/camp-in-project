from flask import Flask, render_template, jsonify, request, redirect, url_for
import hashlib
import datetime
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
SECRET_KEY = 'SPARTA'

import settings
SECRET_KEY = getattr(settings, "SECRET_KEY", "localhost")

from pymongo import MongoClient

client = MongoClient(SECRET_KEY, 27017, authSource="admin")
# client = MongoClient('localhost', 27017)
db = client.cp

## HTML 화면 보여주기
# @app.route('/')
# def home():
#     return render_template('main.html')

@app.route('/')
def home():
    token_receive = request.cookies.get('mytoken')
    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('main.html', user_info=user_info)
    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return render_template('main.html')





##로그인 화면
@app.route('/login')
def login_home():
    return render_template('login.html')


# 주문하기(POST) API
@app.route('/posting')
def posting_home():
    return render_template('posting.html')

# 주문 목록보기(Read) API
@app.route('/api/post', methods=['GET'])
def view_post():
    posts = list(db.posting.find({},{'_id':False}))
    return jsonify({'all_posts': posts})

# 주문 목록보기(Read) API
@app.route('/api/post', methods=['POST'])
def make_post():
    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    name_receive = request.form['name_give']

    # sadjas;lfkja;sdlkfjal;dksjf;lkasadasdsdjf;


    doc = {
        'title': title_receive,
        'content': content_receive,
        'name': name_receive,
    }

    db.posting.insert_one(doc)
    return jsonify({'msg': '저장완료~!'})

#로그인 API
# @app.route('/login')
# def login():
#     msg = request.args.get("msg")
#     return render_template('login.html', msg=msg)

@app.route('/sign_in', methods=['POST'])
def sign_in():
    # 로그인
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']

    pw_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    result = db.users.find_one({'username': username_receive, 'password': pw_hash})

    if result is not None:
        payload = {
         'id': username_receive,
         'exp': datetime.utcnow() + timedelta(seconds=60 * 60 * 24)  # 로그인 24시간 유지
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
 #.decode('utf-8')
        return jsonify({'result': 'success', 'token': token})
    # 찾지 못하면
    else:
        return jsonify({'result': 'fail', 'msg': '아이디또는 비밀번호가 일치하지 않습니다.'})

@app.route('/sign_up/save', methods=['POST'])
def sign_up():
    username_receive = request.form['username_give']
    password_receive = request.form['password_give']
    password_hash = hashlib.sha256(password_receive.encode('utf-8')).hexdigest()
    doc = {
        "username": username_receive,                               # 아이디
        "password": password_hash,                                  # 비밀번호
        "profile_name": username_receive,                           # 프로필 이름 기본값은 아이디
    }
    db.users.insert_one(doc)
    return jsonify({'result': 'success'})


#아이디중복확인
@app.route('/sign_up/check_dup', methods=['POST'])
def check_dup():
    username_receive = request.form['username_give'] #클라이언트로부터 유저네임을 받는다.
    exists = bool(db.users.find_one({"username": username_receive}))
    return jsonify({'result': 'success', 'exists': exists})



if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

