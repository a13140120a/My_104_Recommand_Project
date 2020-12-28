from gensim.models import Word2Vec
import gensim
import jieba
import pymongo
import re
import json

model = gensim.models.Word2Vec.load('resume_model.model')

def isEnglish(s):  # 檢查字元是否為英文
    try:
        s.encode(encoding='utf-8').decode('ascii')
    except UnicodeDecodeError:
        return False
    else:
        return True

def jieba_cut(data, stop_words): # 定義使用結巴程式
    '''
    input:
        data : string
        stop_words: list of stopwords
    output:
        lst_seg : list of words after jieba
    '''

    # 使用結巴斷詞，產生 list of words
    seg_result = jieba.cut(data, cut_all=False)

    # 篩選斷詞，去掉單一中文字
    lst_seg = []

    for i in list(seg_result):
        i = i.strip()
        if len(i) < 1:  # 排除空值
            continue
        elif isEnglish(i) == False and len(i) == 1:  # 排除單一中文字
            continue
        elif i.isdigit() == True:  # 排除數字
            continue
        elif i in stop_words:  # 排除stopwords
            continue

        else:
            lst_seg.append(i)

    return lst_seg

def create_joblist_for_similar(job_list,model):
    user_list = []
    for word in job_list:
        if word in model.wv.vocab.keys():
            user_list.append(word)
        else:
            pass
    return user_list


def mongo_connect_build(db_name, col_name):
    global mycol
    client = pymongo.MongoClient("mongodb://192.168.1.25:27017/")

    db = client[db_name]  # 選擇使用的db,不存在則會在資料輸入時自動建立
    mycol = db[col_name]  # 選擇collection,不存在則會在資料輸入時自動建立


def data_find():
    # 尋找多筆資料
    return mycol.find({}, {'_id': 0})

def string_clean(jobDescription):  # 字串清洗
    '''
    input: a string (original job description)
    output: a string (clean job description)
    '''
    job_desc = jobDescription.split('\n')  # 根據換行符號轉乘 List格式
    job_words = ''

    for words in job_desc:
        words = re.sub(r'[^\w\s]', ' ', words)  # remove all punctuations
        words = re.sub(r'\d+', '', words)  # remove all numbers
        words = words.strip()  # remove white space
        job_words += words

    return (job_words)

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

# cv_data = open_json_file('resume_for_similar.json')

# jieba.load_userdict('jieba_data/Jobcontent_dict.txt')  # 指定辭典檔
#
# # 指定 Stop words檔案
# with open(file='jieba_data/Jobcontent_stopwords.txt', mode='r', encoding="UTF-8") as file:
#     stop_words = file.read().split('\n')
#     stop_words = [i.strip() for i in stop_words]


'''
丟入要匹配的user_list,
用model.n_similarity相似度匹配,
用user_list配對每一筆cv_list,求出相似度建立字典
'''
def job_map_cv(cv_dict,model,user_list):
    rate_dict = {}
    for k,v in zip(cv_dict.keys(),cv_dict.values()):
        rate = model.n_similarity(v,user_list)
        rate_dict[k] = rate
        rate_sort = sorted(rate_dict.items(), key=lambda x:x[1],reverse=True)
        rate_list = list(rate_sort)
    return rate_list

def resume_select_url(rate_list):
    url_list = []
    for i in range(0,10):
         url_list.append('https://www.cakeresume.com/' + str(rate_list[i][0]))
    return url_list


