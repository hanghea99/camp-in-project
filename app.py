import requests
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import settings
SECRET_KEY = getattr(settings, "SECRET_KEY", "localhost")

from pymongo import MongoClient

client = MongoClient(SECRET_KEY, 27017, authSource="admin")
db = client.cp

## HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')



# 주문하기(POST) API
@app.route('/posting')
def posting_home():
    return render_template('posting.html')
@app.route('/posting/posting2/')
def posting_home2():
    return render_template('posting_2.html')

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
    date_receive = request.form['date_give']

    doc = {
        'title': title_receive,
        'content': content_receive,
        'name': name_receive,
        'date': date_receive[8:10] + '일 ' + date_receive[16:18] + '시 ' + date_receive[19:21] + '분'
    }

    db.posting.insert_one(doc)
    return jsonify({'msg': '저장완료~!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
