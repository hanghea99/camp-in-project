import json

from flask import Flask, render_template, jsonify, request, redirect, url_for
import hashlib
import datetime
import jwt
from datetime import datetime, timedelta
import requests
from flask import Flask, render_template, jsonify, request


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
    print(token_receive)

    all_list = list(db.cplist.aggregate([{"$sample": {"size": 27}}, {"$unset": "_id"}]))

    try:
        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('main.html',all_list=all_list, member=True ,user_info=user_info)

    except jwt.ExpiredSignatureError:
        return redirect(url_for("login", msg="로그인 시간이 만료되었습니다."))
    except jwt.exceptions.DecodeError:
        return render_template('main.html',all_list=all_list , member = False)



# 검색 API  
@app.route('/search', methods=['GET'])
def get_list():
    area_receive = request.args.get('area_give')
    search_receive = request.args.get('search_give')
    print(area_receive)
    print(search_receive)

    # 검색 data 추출
    search_list =  list(db.cplist.find({'$and': [ {'area': {"$regex": f"{area_receive}"}} ,{'$or':[ {'title': {"$regex": f"{search_receive}"}},{'comment': {"$regex": f"{search_receive}"}},{'desc': {"$regex": f"{search_receive}"}}]}]},{'_id': False}).sort("views", -1))

    return jsonify({'msg':'sucess',"documents":search_list})

# detail페이지
@app.route('/detail/<id>')
def detail_page(id):
    id=int(id)
    target = db.cplist.find_one({'id': id},{'_id': False})
    current_views = target["views"]
    new_views = current_views + 1
    db.cplist.update_one({"id": id}, {"$set": {"views": new_views}})
    target_row = db.cplist.find_one({'id': id},{'_id': False})
    return render_template('detail.html', target_row=target_row,member=True) 


##로그인 화면
@app.route('/login')
def login_home():
    return render_template('login.html')

# 주문하기(POST) API
@app.route('/posting') # 게시판페이지를 보여주기위한라우트
def posting_home():
    try:
        token_receive = request.cookies.get('mytoken') # 토큰을 받았다면

        payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
        user_info = db.users.find_one({"username": payload["id"]})
        return render_template('posting.html', member=True, user_info=user_info) #정상적으로 로그인되어있다면 게시판에 글쓰기 권한을 주기위해 JINJA2로 로그인이 되어있다면 member가 True로 로그인되어있는 user_info와함께 client쪽으로 전해지게 됨
    except jwt.exceptions.DecodeError:
        return render_template('posting.html', member=False) # 로그인이 되어있지 않다면 즉 가지고 있는 쿠키에 대해서 오류가 나온다면 권한을 주지 않기 위해 member을 False로 전해줌

@app.route('/posting/posting2/<post>') #게시판내에 글 하나를 정해서 보기 위한 페이지를 위한 라우트
def posting_home2(post):
    post = json.loads(post)  #<post>가 json문자열로 변형 되서 넘어와 dict형태로 바꿔주기위해 json import해줌
    name = post['name']
    title = post['title']
    date = post['date']
    content = post['content']
    
 
    return render_template('posting_2.html',name=name,title = title, date = date, content=content) #jinja2 로 데이터를 넘겨줌


@app.route('/api/post2', methods=['GET'])  #db에서 post정보를 가지고 오기위한 API
def posting2():
    title_receive = request.args.get('title_give')
    date_receive = request.args.get('date_give')
    post=list(db.posting.find({'title':title_receive , 'date':date_receive},{'_id':False})) # 게시판에서 등록되는 정보는 제목 userid 내용 작성시간 으로 서로 한번의 검색으로 한가지의 row만 나오는건 시간과 제목일것이라 판단
    ##혹시 db에 저장을 할때 각자의 정보에 번호를 추가 하여 쓴다면 더욱 편리한가? 라는 생각을 나중에함.. -> 동시 접속자가 같은 시간에 글을 남긴다면? db설계를 위한 공부?
    return jsonify({'post': post})


# 게시판 목록보기(Read) API

@app.route('/api/post', methods=['GET'])
def view_post():
    posts = list(db.posting.find({},{'_id':False}))
    return jsonify({'all_posts': posts})

# 게시판 글 쓰기(Write) API
@app.route('/api/post', methods=['POST'])
def make_post():

    title_receive = request.form['title_give']
    content_receive = request.form['content_give']
    name_receive = request.form['name_give']
    date_receive = request.form['date_give']

    doc = {
        'title': title_receive,
        'content': content_receive,
        'name': name_receive,
        'date': date_receive[8:10] + '일 ' + date_receive[16:18] + '시 ' + date_receive[19:21] + '분' #date()로 받아오는 시간은 년 월 일 시 분 초 +a 로 데이터가 넘어오기때문에 필요한 부분만 뽑아오기
    }

    db.posting.insert_one(doc) # db에 저장
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
