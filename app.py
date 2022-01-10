from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

import settings
SECRET_KEY = getattr(settings, "SECRET_KEY", "localhost")

from pymongo import MongoClient

client = MongoClient(SECRET_KEY, 27017, authSource="admin")
db = client.dbusers

## HTML 화면 보여주기
@app.route('/')
def home():
    return render_template('main.html')


# 주문하기(POST) API
@app.route('/order', methods=['POST'])
def save_order():
    sample_receive = request.form['sample_give']
    print(sample_receive)
    return jsonify({'msg': '이 요청은 POST!'})


# 주문 목록보기(Read) API
@app.route('/order', methods=['GET'])
def view_orders():
    sample_receive = request.args.get('sample_give')
    print(sample_receive)
    return jsonify({'msg': '이 요청은 GET!'})


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

