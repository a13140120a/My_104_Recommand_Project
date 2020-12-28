from itemadapter import ItemAdapter
import pymongo
import re
import json
import jieba
from functools import reduce

#第一次過濾
class C104Pipeline:

    def __init__(self):
        self.dict_workExp = {'不拘': 0, '1年以上': 1, '2年以上': 2, '5年以上': 5,
                             '3年以上': 3, '10年以上': 10, '4年以上': 4, '7年以上': 7,
                             '6年以上': 6, '8年以上': 8, '9年以上': 9, '0年以上': 0}


    def clean_jobcategory(self, jobCategory):
        jobCategory_str = ""
        for i in jobCategory:
            jobCategory_str = jobCategory_str + " " + i["description"]
        # 去掉第一個空格
        return jobCategory_str.strip()


    def clean_specialty(self,specialty):
        specialty_str = ""

        if len(specialty) > 0:
            for i in specialty:
                specialty_str = specialty_str + " " + i["description"]
        return specialty_str.strip()


    def clean_major(self,major):
        if len(major) < 1:
            return ""
        else:
            major_str = ""
            for i in major:
                if i.endswith('相關') == True:
                    major_str = major_str + " " + i[0:-2]
                elif i.endswith('學類') == True:
                    major_str = major_str + " " + i[0:-2]
                elif i.endswith('學科類') == True:
                    major_str = major_str + " " + i[0:-3]
                elif i == '日文相關科系':
                    major_str = major_str + " " + '日文科系'
                else:
                    major_str = major_str + " " + i

        return major_str.strip()


    def clean_skill(self,skill):
        skill_str = ""

        if len(skill) > 0:
            for k in skill:
                k_clean = re.sub(u"\\.|k|,|\+|\\(.*?\\)|\\{.*?}|\\[.*?]|\\【.*?】|\\（.*?）|\\(.*?）|\\<.*?>|\d|", "",
                                 k['description'])
                k_clean = k_clean.replace('-', ' ')
                k_clean = k_clean.replace('╱', ' ')
                skill_str = skill_str + " " + k_clean
        return skill_str.strip()


    def clean_language(self,language):
        language_str = ""
        if len(language) > 0:
            for k in language:
                language_str = language_str + " " + k["language"]
        return language_str.strip()


    def clean_workExp(self,workExp):
        workExp_clean = self.dict_workExp[workExp]
        return workExp_clean


    def clean_edu(self,edu):
        lst_clean_edu = []
        dict_edu = {}

        dict_edu['不拘'] = ['高中以下', '高中', '專科', '大學', '碩士', '博士']
        dict_edu['高中以下'] = ['高中以下']
        dict_edu['高中以上'] = ['專科', '大學', '碩士', '博士']
        dict_edu['高中'] = ['高中']
        dict_edu['專科'] = ['專科']
        dict_edu['專科以上'] = ['大學', '碩士', '博士']
        dict_edu['大學'] = ['大學']
        dict_edu['大學以上'] = ['碩士', '博士']
        dict_edu['碩士'] = ['碩士']
        dict_edu['碩士以上'] = ['博士']
        dict_edu['博士'] = ['博士']
        edu_split = edu.split('、')
        for i in edu_split:
            clean_edu = dict_edu[i]
            lst_clean_edu += clean_edu

        lst_clean_edu = list(set(lst_clean_edu))  # remove duplicate element in a list
        return lst_clean_edu


    def clean_salary(self,salary):
        salary_clean = []
        if salary["salary"].startswith('時薪'):
            salary_clean.append('時薪')
        elif salary["salary"].startswith('日薪'):
            salary_clean.append('日薪')
        elif salary["salary"].startswith('月薪'):
            salary_clean.append('月薪')
        elif salary["salary"].startswith('年薪'):
            salary_clean.append('年薪')
        elif salary["salary"].startswith('待遇面議'):
            salary_clean.append('待遇面議')
        elif salary["salary"].startswith('論件計酬'):
            salary_clean.append('論件計酬')
        else:
            salary_clean.append('')
        salary_clean.append(salary["salaryMax"])
        salary_clean.append(salary["salaryMin"])
        return salary_clean


    def clean_certificate(self,certificate):
        certificate_str = ""
        if len(certificate) > 0:
            for k in certificate:
                if k != None:
                    k_clean = re.sub(u"\\.|k|,|\+|\\(.*?\\)|\\{.*?}|\\[.*?]|\\【.*?】|\\（.*?）|\\(.*?）|\\<.*?>||", "", k)
                    certificate_str = certificate_str + " " + k_clean
        return certificate_str.strip()


    def string_clean(self, jobDescription):
        '''
        input: string
        output: string
        '''
        job_desc = jobDescription.split('\n')
        job_words = ''

        for words in job_desc:
            words = words.replace('\t', ' ').replace('\r', ' ')
            words = re.sub(r'[^\w]|\s',' ', words)  # remove all punctuations
            words = re.sub(r'[^a-zA-Z]*\d[^a-zA-Z]', ' ', words)  # remove all numbers
            words = words.strip() # remove white space
            words += ' '
            job_words += words

        return (job_words)


    def process_item(self, item, spider):
        item["other"] = self.string_clean(item["other"])
        item["jobCategory"] = self.clean_jobcategory(item["jobCategory"])
        item["jobDescription"] = self.string_clean(item["jobDescription"])
        item["specialty"] = self.clean_specialty(item["specialty"])
        item["major"] = self.clean_major(item["major"])
        item["skill"] = self.clean_skill(item["skill"])
        item["language"] = self.clean_language(item["language"])
        item["workExp"] = self.clean_workExp(item["workExp"])
        item["edu"] = self.clean_edu(item["edu"])
        item["salary"] = self.clean_salary(item["salary"])
        item["certificate"] = self.clean_certificate(item["certificate"])
        return item

#第二次過濾(合併欄位與jieba 斷詞)
class MongoDBPipeline:

    def __init__(self):
        with open(file='./Jobcontent_stopwords.txt',mode='r', encoding="UTF-8") as file:
            stop_words = file.read().split('\n')
        self.stop_words = [i.strip() for i in stop_words]
        self._ = jieba.load_userdict('./Jobcontent_dict.txt')


    def open_spider(self, spider):
        db_uri = spider.settings.get('MONGODB_URI', 'mongodb://192.168.6.128:27017')
        db_name = spider.settings.get('MONGODB_DB_NAME', 'Topic_104')
        self.db_client = pymongo.MongoClient('mongodb://192.168.6.128:27017')
        self.db = self.db_client[db_name]


    def process_item(self, item, spider):
        '''

        :input:  dict of item
        :output: dict to mongodb
        '''
        insert_item = {}
        concate_string = self.concate_column(item)
        jieba_cut_list = self.jieba_cut(concate_string)
        #把斷詞後的結果塞進jieba_cut_list 欄位
        item["jieba_cut_list"] = jieba_cut_list
        self.insert_Row_data(item)
        return item


    # combine 所需欄位
    def concate_column(self,item):
        """

        :param item: dict of item
        :return: a string after combining
        """
        concate_list = []
        concate_list.append(item['other'])
        concate_list.append(item["jobCategory"])
        concate_list.append(item['jobDescription'])
        concate_list.append(item["specialty"])
        concate_list.append(item["major"])
        concate_list.append(item["skill"])
        concate_list.append(item["language"])
        concate_list.append(item["certificate"])

        concate_string = reduce(lambda x,y: x.strip() + y.strip() + " ", concate_list)
        return concate_string.strip()


    def jieba_cut(self, data):
        """
        :input a string of a job after combining
        """
        jieba_cut_list = [*jieba.cut(data, cut_all=False)]
        jieba_cut_list = [*filter(self.word_filter, jieba_cut_list)]
        return jieba_cut_list


    def word_filter(self, word):
        """
        :input a word to self.cut_list after filtering
        """
        word = word.strip()
        if len(word) < 1:  # 排除空值
            return False
        elif word in self.stop_words:  # 排除stopwords
            return False
        elif self.isEnglish(word) == False and len(word) == 1:  # 排除單一中文字
            return False
        elif word.isdigit() == True:  # 排除數字
            return False
        else:
            return True

    # 檢查字元是否為英文
    def isEnglish(self, string):
        try:
            string.encode(encoding='utf-8').decode('ascii')
        except UnicodeDecodeError:
            return False
        else:
            return True


    def insert_Row_data(self, item):
        item = dict(item)
        self.db.Row_data.insert_one(item)


    def close_spider(self, spider):
        self.db_client.close()