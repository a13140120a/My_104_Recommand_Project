import scrapy


class C104Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    other = scrapy.Field()
    jobCategory = scrapy.Field()
    jobDescription = scrapy.Field()
    jobName = scrapy.Field()
    specialty = scrapy.Field()
    major = scrapy.Field()
    skill = scrapy.Field()
    language = scrapy.Field()
    addressRegion = scrapy.Field()
    workExp = scrapy.Field()
    edu = scrapy.Field()
    salary = scrapy.Field()
    certificate = scrapy.Field()
    appearDate = scrapy.Field()
    custName = scrapy.Field()
    #於主程式定義
    jobCat_main = scrapy.Field()
    #於MongoDBPipeline 定義
    jieba_cut_list = scrapy.Field()

