import jieba
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from joblib import dump, load
import pickle
from flask import Flask
from flask import request
from finalcv import *
import time
from flask import render_template

#app = Flask(__name__,static_url_path = "/素材" , static_folder = "./素材/")
app = Flask(__name__)


jieba.load_userdict('Jobcontent_dict.txt')
# 指定 Stop words檔案
with open(file='Jobcontent_stopwords.txt', mode='r', encoding="UTF-8") as file:
    stop_words = file.read().split('\n')
    stop_words = [i.strip() for i in stop_words]




@app.route('/html2')
def html2():
    return render_template('html2.html')

@app.route('/submit', methods =['POST'])
def submit():
    tStart = time.time()
    area = request.values['area']
    year = request.values['year']
    edu = request.values['edu']
    work = request.values['work']

    test_string = string_clean(work)
    test_cv = jieba_cut(test_string, stop_words)
    test_cv_category = cv_category_predict(test_cv)
    # print(test_cv_category)

    # 2. load Job JSON data and filter it
    dict_jobs = open_json_file('104_flask.json')
    jobs_query = select_jobs(dict_jobs, str(test_cv_category), area, int(year), edu)
    if len(jobs_query) == 0:
        tEnd = time.time()  # 計時結束
        # 列印結果
        print("It cost %f sec" % (tEnd - tStart))
        return '您的搜尋結果找不到職缺，請放寬篩選條件'
    else:

        # 3. compute similarity
        cv_BOW = turn_content_BOW(test_cv)

        # 4. show result

        model_train = Word2Vec.load('Word2Vec.model')
        try:
            L = show_recommendation_result(cv_BOW, jobs_query, model_train)
            tEnd = time.time()  # 計時結束
            # 列印結果
            print("It cost %f sec" % (tEnd - tStart))
            return render_template('html2.html', content1=str(test_cv_category), L = L)
        except:
            tEnd = time.time()  # 計時結束
            # 列印結果
            print("It cost %f sec" % (tEnd - tStart))
            return "推薦失敗，請重新輸入"







if __name__ == '__main__':
    app.run(debug = True)
