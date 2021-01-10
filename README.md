# My_104_Recommand_Project

本次專案感謝: 
 1. 組長:張維芸
 2. 方韋智 
 3. 李鴻昇
 4. 董彥廷 
 5. 范謙恆
 我是副組長: 王炫斐


本次專案採用LineBot 介面呈現，其中又可分成四個部分，分別是:
  1. 履歷匹配職缺功能: 使用者輸入履歷內容，匹配出合適之職位  
  2. 職缺匹配履歷功能: 人資可以上傳職業名稱，條件，以及工作內容使系統匹配出合適的履歷
  3. 職缺分析視覺化: 使用tableau 分析目前台灣職缺狀況
  4. 拍照辨識功能: 使用者可以藉由LineBot 上傳大頭照，辨識出是否符合證件照規格
  
以下是本次專案運用技術:
  1. 利用爬蟲對104進行爬取職缺資料
    * 2020/12/28更新: 改為使用scrapy 爬蟲框架，並於itempipeline 直接做初步清洗
    * 2020/12/29更新: 增加每日爬取的功能
  2. 利用jupyter notebook 清洗資料
    * 2020/12/28更新: 已更改到scrapy 的itempipeline
  2. 利用scikit learn CountVectorize 將文字像量化之後使用樸素貝葉斯分類
  3. 分類完之後再使用gensim word2vec 做職缺的相似度計算
  4. 使用OpenCV 做為影像辨識部分，先取特徵框，再依特徵框內雜質多寡辨識是否符合證件照規範
  5. 建置Flask 網頁並佈署至Heroku 上，供使用者使用，以連結LineBot
     * 2021/1*10 更新: Flask 改為使用Django架設網頁
  6. 使用Docker 建置LineBot 聊天機器人，分別連接到Flask 網頁以及 Tableau 職缺分析
  7. Tableau 職缺分析

連結:
  1. [履歷尋找職缺網站](http://for-workers.herokuapp.com/html2)
  2. [職缺尋找履歷網站](http://for-company-104.herokuapp.com/forcompany)
  3. [爬蟲及初步資料清洗](https://github.com/a13140120a/My_104_Recommand_Project/tree/master/c104/c104)
  4. [建模部分](https://github.com/a13140120a/My_104_Recommand_Project/tree/master/create_model)
  5. [LineBot串接Flak、OpenCV、Tableau](https://github.com/a13140120a/My_104_Recommand_Project/tree/master/linebot-opencv)
  6. [Demo示範影片連結](https://www.youtube.com/watch?v=FiGBseq4icc&feature=youtu.be&ab_channel=%E8%AC%99%E6%81%86%E8%8C%83)
  
