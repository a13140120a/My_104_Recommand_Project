from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import preprocessing
from gensim.models import Word2Vec
from joblib import dump, load
import pickle, jieba, re
from .models import Job

jieba.load_userdict('Jobcontent_dict.txt')
model_train = Word2Vec.load('app_104/model_data/word2vec.model')

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


def jieba_cut(data):
    with open(file='Jobcontent_stopwords.txt', mode='r', encoding="UTF-8") as file:
        stop_words = file.read().split('\n')

    seg_result = jieba.cut(data, cut_all=False)

    # 篩選斷詞，去掉單一中文字
    lst_seg = []

    for word in list(seg_result):
        word = word.strip()
        if len(word) < 1:  # 排除空值
            continue
        elif word in stop_words:  # 排除stopwords
            continue
        elif isEnglish(word) == False and len(word) == 1:  # 排除單一中文字
            continue
        else:
            lst_seg.append(word)

    return lst_seg


def cv_category_predict(cv_data):
    vectorizer = pickle.load(open("app_104/model_data/vectorizer.pickel", "rb"))
    transform_content = vectorizer.transform([cv_data])  # CountVectorizer transform (must be a list)
    X_test = transform_content.toarray()
    model = load('app_104/model_data/MultinomialNB.joblib')
    le = pickle.load(open("app_104/model_data/le.pickel", "rb"))
    y_pred = model.predict(X_test)  # MultinomialNB transform
    y_pred_category = le.inverse_transform(y_pred)
    y_pred_category = y_pred_category[0]
    return y_pred_category

# 將結巴後的斷詞，利用CountVectorizer轉換，確認字詞在模型內
def turn_content_BOW(content):

    vectorizer = pickle.load(open("app_104/model_data/vectorizer.pickel", "rb"))
    transform_content = vectorizer.transform([content])
    X_content = vectorizer.inverse_transform(transform_content)[0].tolist()
    return X_content


# 計算 Word2Vec similarity
def compute_similarity(cv_BOW, job_BOW):
    global model_train
    job_prob = model_train.wv.n_similarity(cv_BOW, job_BOW)
    return job_prob


# 定義 recommendation function，顯示10筆結果
def show_recommendation_id(cv_clean, jobs_query):
    cv_BOW = turn_content_BOW(cv_clean)
    # 確認BOW內的字詞包含在模型內
    cv_BOW_for_Word2Vec = []
    model_train_vocab = set(model_train.wv.vocab.keys())
    for i in cv_BOW:
        if i in model_train_vocab:
            cv_BOW_for_Word2Vec.append(i)

    # 將職缺資料轉成 Word2Vec格式
    lst_jobs_content = [] #裝 jiebaCutList_join
    lst_jobs_url = [] #裝url

    for data in jobs_query:
        lst_jobs_content.append(data.jiebaCutList_join)
        lst_jobs_url.append(data.url)

    # 計算所有CV與職缺的similarity，排序後儲存10筆相關度最高職缺
    dict_prob_id = {}
    for index, j in enumerate(lst_jobs_content):
        job_url = lst_jobs_url[index]
        job_prob = compute_similarity(cv_BOW_for_Word2Vec, j.split(" "))
        dict_prob_id[job_prob] = job_url
    result_id_list = [(k, dict_prob_id[k]) for k in sorted(dict_prob_id.keys(), reverse=True)[0:10]]

    return result_id_list


def recommendation_id_2_result(top10_recommendation_id):
    result_list = []
    for _id in top10_recommendation_id:
        # _id:  (0.7484418, '74c0l')
        queryset = Job.objects.filter(url=_id[1])
        result_list.append(queryset[0])
    return result_list