#引入套件(pip install flask)
from flask import *
from dataselect import *
app = Flask(__name__)
#第一個函數進入網站

@app.route('/html2')
def html2():
    return render_template('html2.html')



#第2個函數是在按下確認送出(submit)之後要執行的
@app.route('/submit', methods =['POST'])
def submit():
    category = request.values["occupations"]#把所有對應的值(values)抓出
    job = request.values['job']
    area = request.values["regions"]
    year = request.values['years']
    work = request.values['work']

    # mysql_select_data(area, year, category)

   ############{{{{把job輸入資料分析師,years選擇無經驗,work輸入資料分析}}}}}}###########
    #三個都有回傳成功就會是good,任何一個沒抓到就是bad
    if category =='客服╱門市╱業務╱貿易類' and job =="資料分析師" and area =="台北市" and year == "0年" and work == "資料分析":
        return "GOOD !"
    else:
        return "BAD !"
    # return "輸入完成:職稱為{}".format(work), "，年資為{}".format(years), "，履歷:{}".format(work)


if __name__ == '__main__':
    app.debug = True
    app.run()

#程式開始跑之後進入網站網址
#http://127.0.0.1:5000/html2






#<p><input type = 'textbox'   class='form-control' style="font-size:16px;padding:100px"  name = 'work'  placeholder="請詳述您的工作經歷"></p>
