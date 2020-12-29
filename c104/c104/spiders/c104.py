import scrapy
import random
import json
from c104.items import C104Item

class C104Spider(scrapy.Spider):
    name = 'c104'
    allowed_domains = ['www.104.com.tw']

    #第一次爬取全部資料，之後只爬取當天更新資料
    First_time = False

    def __init__(self,*args, **kwargs):
        #定義 start_urls
        super(C104Spider, self).__init__(*args, **kwargs)
        self.start_urls = []
        with open("c104/spiders/104area.txt", "r")as f:
            self.areas =  f.read().split("\n")
        with open(file='./JobCat.json', mode='r', encoding="UTF-8") as file:
            self.JobCat = json.loads(file.read(),encoding='utf-8-sig')


        # 一次最多只能顯示150頁
        # 所以依據薪水區分成0~37999不包含面議，38000~40000包含面議，40000以上不包含面議，讓所有的工作可以被撈出來
        restrict1 = 'https://www.104.com.tw/jobs/search/list?sctp=M&page=0&area={area}&scmax=37999&sceng=0'
        restrict2 = 'https://www.104.com.tw/jobs/search/list?sctp=M&page=0&area={area}&scmax=40000&scmin=38000&sceng=1'
        restrict3 = 'https://www.104.com.tw/jobs/search/list?sctp=M&page=0&area={area}&scmin=40000&sceng=0'

        if self.First_time:
            for area in self.areas:
                self.start_urls.append(restrict1.format(area=area))
                self.start_urls.append(restrict2.format(area=area))
                self.start_urls.append(restrict3.format(area=area))

        else:
            for area in self.areas:
                self.start_urls.append(restrict1.format(area=area)+"&isnew=0")
                self.start_urls.append(restrict2.format(area=area)+"&isnew=0")
                self.start_urls.append(restrict3.format(area=area)+"&isnew=0")

    def parse(self, response):
        #先抓出totalpage, 再一頁一頁抓資料(直接撈json檔)
        totalpage=int(response.json()["data"]["totalPage"])
        for page in range(1,totalpage+1):
            page_url= response.url+"&page={}".format(page)
            yield scrapy.Request(page_url,callback=self.parse2)

    def parse2(self,response):
        urls = response.json()["data"]["list"]
        for i in urls:
            url = i["link"]["job"]
            url = url.split('?')[0].split('/')[-1]
            if url != "trans_job_to_case.cfm":
                url  = "https://www.104.com.tw/job/ajax/content/" + url
                yield scrapy.Request(url,callback=self.parse3)

    def parse3(self,response):
        item = C104Item()
        item["_id"] = response.json()["data"]["header"]["analysisUrl"].split("/")[-1]
        item["other"] = response.json()["data"]["condition"]["other"]
        item["jobCategory"] = response.json()["data"]["jobDetail"]["jobCategory"]
        item["jobDescription"] = response.json()["data"]["jobDetail"]["jobDescription"]
        item["jobName"] = response.json()["data"]["header"]["jobName"]
        item["specialty"] = response.json()["data"]["condition"]["specialty"]
        item["major"] = response.json()["data"]["condition"]["major"]
        item["skill"] = response.json()["data"]["condition"]["skill"]
        item["language"] = response.json()["data"]["condition"]["language"]
        item["addressRegion"] = response.json()["data"]["jobDetail"]["addressRegion"]
        item["workExp"] = response.json()["data"]["condition"]["workExp"]
        item["edu"] = response.json()["data"]["condition"]["edu"]
        item["salary"] = {"salary":response.json()["data"]["jobDetail"]["salary"],
                          "salaryMax":response.json()["data"]["jobDetail"]["salaryMax"],
                          "salaryMin":response.json()["data"]["jobDetail"]["salaryMin"]}
        item["certificate"] = response.json()["data"]["condition"]["certificate"]
        item["appearDate"] = response.json()["data"]["header"]["appearDate"]
        item["custName"] = response.json()["data"]["header"]["custName"]
        item["jobCat_main"] = self.code_to_jobCategory(response.json()["data"]["jobDetail"]["jobCategory"][0]["code"])
        yield item

    def code_to_jobCategory(self,code):
        jobCategory_code = {}
        for i in self.JobCat:
            jobCategory_code[i["no"]] = i["des"]
        # 前6碼+四個0
        key = code[0:6] + "0000"
        return jobCategory_code[key]