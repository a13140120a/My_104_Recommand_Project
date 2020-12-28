from flask import *
import resume_for_similar
import gensim
import jieba

app = Flask(__name__)
@app.route('/forcompany')
def page():
    return render_template('forcompany.html')

@app.route('/submit', methods =['POST'])
def submit():
    title = request.values["title"]#把所有對應的值(values)抓出
    skill = request.values['skill']
    detail = request.values['detail']
    des = title + skill + detail


    model = gensim.models.Word2Vec.load('resume_model.model')
    jieba.load_userdict('Jobcontent_dict.txt')
    data = resume_for_similar.string_clean(des)
    print(data)
    # 指定 Stop words檔案
    with open(file='Jobcontent_stopwords.txt', mode='r', encoding="UTF-8") as file:
        stop_words = file.read().split('\n')
        stop_words = [i.strip() for i in stop_words]
    job_list = resume_for_similar.jieba_cut(data,stop_words)
    user_list = resume_for_similar.create_joblist_for_similar(job_list,model)
    cv_data = resume_for_similar.open_json_file('resume_for_similar.json')
    rate_list = resume_for_similar.job_map_cv(cv_data,model,user_list)
    url_list = resume_for_similar.resume_select_url(rate_list)
    no=['適合您的履歷1','適合您的履歷2','適合您的履歷3','適合您的履歷4','適合您的履歷5','適合您的履歷6','適合您的履歷7','適合您的履歷8','適合您的履歷9','適合您的履歷10']




    return render_template('forcompany.html', L = zip(no,url_list))
    # if title == "資料分析師" and area == "台北市" and salary == '1' and skill == '123' and detail == "123" :
    #     return "Good!"
    # else:
    #     return "Bad!"

if __name__ == '__main__':
    app.debug = True
    app.run()