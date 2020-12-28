#引入套件(pip install flask)
from flask import *
from logging import DEBUG

from datetime import datetime

import json

from flask_pymongo import PyMongo
import pymongo

app = Flask(__name__)
#連上mongodb的localhost
app.config["MONGO_URI"] = "mongodb://localhost:27017/Topic_105"
mongo = PyMongo(app)

# app.config.update(
#
# MONGO_URI='mongodb://localhost:27017/flask',
#
# MONGO_PORT=27017
#
# )
#mongodb連線
def mongo_connect_build():
    global mycol
    client = pymongo.MongoClient("mongodb://192.168.1.25:27017/")
    # client = pymongo.MongoClient(host="mongodb", port=27017)

    # 選擇使用的db,不存在則會在資料輸入時自動建立

    db = client['Topic_105']
    # 選擇collection,不存在則會在資料輸入時自動建立
    mycol = db["TestJobs"]

@app.route('/html2')
def html2():

    return render_template('html2.html')



@app.route('/submit', methods =['POST'])
def submit():
    job = request.values['job']    #把所有對應的值(values)抓出
    years = request.values['years']
    work = request.values['work']


#串成json
    j = {

        'job': job,

        'years': years,

        'work': work

    }

    #insert到指定db(mycol)
    mycol.insert_one(j)
    print("Insert Succeessfullyˊˇˋ")
    #return "輸入完成:職稱為{}".format(job),"，年資為{}".format(years),"，履歷:{}".format(work)

    if job =="資料分析師" and years == "0年" and work == "資料分析":
        return "GOOD !"
    else:
        return "BAD !"




if __name__ == '__main__':
    mongo_connect_build()
    app.debug = True
    app.run()
      # 連線mongodb


#程式開始跑之後進入網站網址
#http://127.0.0.1:5000/html2
