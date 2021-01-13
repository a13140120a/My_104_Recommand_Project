from django.core.management.base import BaseCommand, CommandError
import pymongo
import pprint
import random
import json
from app_104.models import Job



class Command(BaseCommand):
    # 建立連線
    db_name = 'Topic_104'
    col_name = 'Row_data'
    host = "mongodb://192.168.160.130:27017/"

    client = pymongo.MongoClient(host)
    db = client[db_name]
    mycol = db[col_name]

    def handle(self, *args, **options):
        job_lst = self.mycol.find({},{"jobName":1,
                                 "addressRegion":1,
                                 "edu":1,
                                 "custName":1,
                                 "jobCat_main":1,
                                 "workExp":1,
                                 "jieba_cut_list":1})
        job_lst = [*job_lst]

        def load_data(one_of_job_lst):
            job = Job(url=one_of_job_lst["_id"],
                      jobName=one_of_job_lst["jobName"],
                      addressRegion=one_of_job_lst["addressRegion"],
                      jobCat_main=one_of_job_lst['jobCat_main'],
                      workExp=one_of_job_lst["workExp"],
                      custName=one_of_job_lst["custName"],
                      jiebaCutList_join=" ".join(one_of_job_lst["jieba_cut_list"]),
                      edu = " ".join(one_of_job_lst["edu"])
                      )
            job.save()
            self.stdout.write(self.style.SUCCESS('Successfully "%s"' % one_of_job_lst))
            print(one_of_job_lst)

        #[*map(load_data,job_lst)]
        [*map(load_data,random.sample(job_lst,k=20000))]

#Job.objects.all()[0].data