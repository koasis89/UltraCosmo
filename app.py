from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
#client = MongoClient('mongodb://ultracosmo:milkyhair10@localhost', 27017)
client = MongoClient('localhost', 27017)
db = client.dbsparta

## HTML을 주는 부분
@app.route('/')
def home():
   return render_template('index.html')

@app.route('/memo', methods=['GET'])
def listing():
    articles = list(db.articles.find({}, {'_id': False}))
    return jsonify({'all_articles': articles})

@app.route('/search', methods=['POST'])
def listingSearch():
    search_receive = request.form['search_give']
    print(search_receive)
    articles = list(db.articles.find({'comment': {'$regex': search_receive}}, {'_id': False}))
    print(articles)
    return jsonify({'all_articles': articles})

## API 역할을 하는 부분
@app.route('/memo', methods=['POST'])
def saving():
    url_receive = request.form['url_give']
    comment_receive = request.form['comment_give']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
    data = requests.get(url_receive, headers=headers)

    soup = BeautifulSoup(data.text, 'html.parser')
    try:
        title = soup.select_one('meta[property="og:title"]')['content']
        image = soup.select_one('meta[property="og:image"]')['content']
        desc = soup.select_one('meta[property="og:description"]')['content']
        doc = {
            'url': url_receive,
            'title': title,
            'image': image,
            'desc': desc,
            'comment': comment_receive
        }
        db.articles.insert_one(doc)
        return jsonify({'result':1})
    except:
        title = url_receive
        image = "./static/ogimage.jpg"
        desc = ""
        doc = {
            'url': url_receive,
            'title': title,
            'image': image,
            'desc': desc,
            'comment': comment_receive
        }
        db.articles.insert_one(doc)
        return jsonify({'result': 0})
@app.route('/delete', methods=['POST'])
def deleting():
    comment_receive = request.form['comment_give']
    print(comment_receive)
    try:
        articles = list(db.articles.find({'comment': comment_receive}))
        print(articles)
        cnt = db.articles.    cnt = db.articles.delete_one({'comment': comment_receive})
        print("delete success", cnt)
        return jsonify({'result': 1})
    except:
        print("delete fail")
        return jsonify({'result': 0})

if __name__ == '__main__':
   app.run('0.0.0.0',port=5000,debug=True)