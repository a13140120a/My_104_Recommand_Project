import pymongo
import pprint
import random
import json
#
# 建立連線
db_name = 'Topic_104'
col_name = 'Row_data'
host = "mongodb://192.168.160.130:27017/"

client = pymongo.MongoClient(host)
db = client[db_name]
mycol = db[col_name]

#{"workExp":{"$gt":10}
job_lst = mycol.find({},{"jobName":1,
                         "addressRegion":1,
                         "edu":1,
                         "custName":1,
                         "jobCat_main":1,
                         "workExp":1,
                         "jieba_cut_list":1})

# print(len([*job_lst]))

## 先insert job
## 再insert edu
for i in random.sample([*job_lst],k=2000) :

    job = Job(data={"_id":i["_id"],
              "jobName":i["jobName"],
              "addressRegion":i["addressRegion"],
              "edu":i["edu"],
              "jobCat_main":i['jobCat_main'],
              "workExp":i["workExp"],
              "custName":i["custName"],
              "jieba_cut_list":i["jieba_cut_list"]}
              )
    job.save()
    print(i)

from app_104.models import Job
Job.objects.all()[0].data