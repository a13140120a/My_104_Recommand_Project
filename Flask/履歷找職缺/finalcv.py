from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from gensim.models import Word2Vec
from sklearn import preprocessing
from joblib import dump, load
import pandas as pd
import pickle
import jieba
import json
import re
import time


def string_clean(CV_data):
    '''
    input: string (original CV description)
    output: string (clean CV description)
    '''
    job_desc = CV_data.split('\n')  # 根據換行符號轉乘 List格式
    job_words = ''

    for words in job_desc:
        words = words.replace('\t', ' ').replace('\r', ' ')
        words = re.sub(r'[^\w\s]', ' ', words)  # remove all punctuations
        words = re.sub(r'\d+', ' ', words)  # remove all numbers
        words = words.strip()  # remove white space
        words += ' '
        job_words += words

    return (job_words)


def isEnglish(s):  # 檢查字元是否為英文
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True


def jieba_cut(data, stop_words):
    # 使用結巴斷詞
    seg_result = jieba.cut(data, cut_all=False)

    # 篩選斷詞，去掉單一中文字
    lst_seg = []

    for i in list(seg_result):
        i = i.strip()
        if len(i) < 1:  # 排除空值
            continue
        elif i in stop_words:  # 排除stopwords
            continue
        elif isEnglish(i) == False and len(i) == 1:  # 排除單一中文字
            continue
        else:
            lst_seg.append(i)

    return lst_seg


def cv_category_predict(cv_data):
    cv_data = [" ".join(cv_data)]
    vectorizer = pickle.load(open("vectorizer.pickel", "rb"))
    transform_content = vectorizer.transform(cv_data)  # CountVectorizer transform
    X_test = transform_content.toarray()
    # vectorizer.inverse_transform(X_test)

    model = load('MultinomialNB.joblib')
    y_pred = model.predict(X_test)  # MultinomialNB transform

    le = pickle.load(open("le.pickel", "rb"))
    y_pred_category = le.inverse_transform(y_pred)
    y_pred_category = y_pred_category[0]

    return y_pred_category

def open_json_file(CACHE_FNAME):
    try:
        cache_file = open(CACHE_FNAME, 'r', encoding='utf-8-sig')
        cache_contents = cache_file.read()
        CACHE_DICTION = json.loads(cache_contents, encoding='utf-8-sig')
        cache_file.close()
        return CACHE_DICTION

    except:
        CACHE_DICTION = {}
        return CACHE_DICTION



def select_jobs(job_dict, category, area=None, workExp=None, edu=None):
    df = pd.DataFrame(job_dict)
    df = df[df['jobCat_main'] == category]

    if area is not None:
        df = df[df['Work_area_clean'] == area]

    if workExp is not None:
        lst_workExp = list(i for i in range(workExp, 11))
        df = df[df['workExp_clean'].astype(int).isin(lst_workExp)]

    if edu is not None:
        df = df[df['Edu_clean'].str.contains("大學")]

    filter_result = df.values.tolist()

    # 將資料儲存成flask可用的dictionary格式

    dict_data = {}

    for i in filter_result:
        jobURL, Job_Name, Company, Job_Description, concate_jieba = i[0], i[1], i[2], i[7], i[8]
        dict_data[jobURL] = {
            'Job_Name': Job_Name,
            'Company': Company,
            'Job_Description': Job_Description,
            'concate_jieba': concate_jieba}

    return dict_data

def turn_content_BOW(content):
    X_content = [ " ".join(content)]
    vectorizer = pickle.load(open("vectorizer.pickel", "rb"))
    transform_content = vectorizer.transform(X_content)
    X_content = vectorizer.inverse_transform(transform_content)[0].tolist()
    return X_content

def compute_similarity(cv_BOW, job_BOW, model_train):
    job_prob = model_train.wv.n_similarity(cv_BOW, job_BOW)
    return job_prob


def show_recommendation_result(cv_clean, jobs_query, model_train):
    cv_BOW = turn_content_BOW(cv_clean)
    cv_BOW_for_Word2Vec = []
    for i in cv_BOW:
        if i in list(model_train.wv.vocab.keys()):
            cv_BOW_for_Word2Vec.append(i)

    cv_BOW = cv_BOW_for_Word2Vec

    lst_jobs_content = []
    lst_jobs_url = []

    for k, v in jobs_query.items():
        split_data = v['concate_jieba'][0].split(',')
        lst_jobs_content.append(split_data)
        lst_jobs_url.append(k)

    dict_prob_id = {}

    for i, j in enumerate(lst_jobs_content):
        job_url = lst_jobs_url[i]
        job_prob = compute_similarity(cv_BOW, j, model_train)
        dict_prob_id[job_prob] = job_url
    result = [(k, dict_prob_id[k]) for k in sorted(dict_prob_id.keys(), reverse=True)[0:10]]

    L=[]
    n = 1
    for i, j in result:
        items = jobs_query[j]
        items.update({'job_url': 'https://www.104.com.tw/job/' + j})
        items.update({'Number': '推薦您的職缺' + str(n)})

        # prob, url = i[0], i[1]
        # job_dict = jobs_query[url]
        # lst_result = [prob, job_dict['Job_Name'], job_dict['Company'], job_dict['Job_Description'], 'https://www.104.com.tw/job/'+url, '推薦您的職缺'+str(n)]
        L.append(items)
        n+=1

    return L









def main():
    tStart = time.time()


    jieba.load_userdict('Jobcontent_dict.txt')  # 指定辭典檔
    with open(file='Jobcontent_stopwords.txt', mode='r', encoding="UTF-8") as file:
        # 排除字元表單 stopword, 開啟 'Jobcontent_stopwords.txt'檔案
        stop_words = file.read().split('\n')
        stop_words = [i.strip() for i in stop_words]

    test_string = '''
    最近工作\n\n公司：\tXX醫院\t行業：\t醫療/護理/衛生\n職位：\t醫生\n
    最高學歷\t\n最高學歷\n\n學校：\t中醫藥大學\n學歷：\t本科\t專業：\t\n
    醫藥學\n工作經驗\t\n工作經驗\n\n公司：\t\nXX醫院\n2012/7–2017/7\n職位：\t醫生\n
    行業：\t醫療/護理/衛生\n部門：\t醫藥部\n工作內容：\n
    1.了解各種儀器設備的使用方法。2.參與手術工作，鍛煉手術操作能力。
    3.熟悉實際操作中所出現的問題並通過各種方法避免和克服。4.勤學好問，大膽展示自我
    ，學會了要禮貌待人，要踏實幹事，要提高個人綜合素質。\n教育經歷\t\n教育經歷\n\n學校：\t\n
    中醫藥大學\n2007/9–2011/6\n專業：\t醫藥學\t本科\t\n自我評價\t\n自我評價\n\n在校期間，
    學習了解剖學、生物化學、生理學、病理學、精神學等等課程，在校成績優異，擔任學生幹部的職務，
    曾多次獲得過學校獎學金，平時積極主動參加校內活動，曾負責在專業內組織過醫學演講。學習態度端正，
    能夠主動學習，認真對待每一次學習的機會，我希望在學習理論知識的同時，能夠增強自己的實踐經驗，
    我 相信沒有做不到，只有不想做。\n求職意向\t\n求職意向\n\n到崗時間：\t一個月之內\n工作性質：\t
    全職\n希望行業：\t醫療/護理/衛生\n目標地點：\t北京\n期望月薪：\t面議/月\n目標職能：\t醫生\n
    語言能力\t\n語言能力\n\n英語：\t\n良好\n\n聽說：\t\n良好\n\n讀寫：\t\n良好\n\n證書\t\n證書\n\n大學英語四級
    '''



    # 1. input CV data, data cleaning, jieba, prediction
    test_string = string_clean(test_string)
    test_cv = jieba_cut(test_string, stop_words)
    test_cv_category = cv_category_predict(test_cv)
    # print(test_cv_category)

    # 2. load Job JSON data and filter it
    dict_jobs = open_json_file('104_flask.json')
    jobs_query = select_jobs(dict_jobs, str(test_cv_category), '台北市', 0, '大學')

    # 3. compute similarity
    cv_BOW = turn_content_BOW(test_cv)



    # 4. show result

    model_train = Word2Vec.load('Word2Vec.model')
    list_ten_result = show_recommendation_result(cv_BOW, jobs_query, model_train)
    # final_result = get_cv_jobs_similarity(cv_BOW, jobs_query)

    for i in list_ten_result:
        print(i)
    tEnd = time.time()
    print("It cost %f sec" % (tEnd - tStart))  # 會自動做近位



if __name__ == '__main__':
    main()