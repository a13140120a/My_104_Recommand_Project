# coding: utf-8

from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler

# 引用無效簽章錯誤
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, ImageMessage, TextSendMessage, ImageSendMessage, TemplateSendMessage, FlexSendMessage
from linebot.models import RichMenu

import json, cv2
import numpy as np
from opcv2 import readheadshots


secretFileContentJson=json.load(open("./line_secret_key",'r',encoding='utf8'))

line_bot_api  = LineBotApi(secretFileContentJson.get("channel_access_token"))

handler       = WebhookHandler(secretFileContentJson.get("secret_key"))

face_cascade  = cv2.CascadeClassifier('./123/data/haarcascade_frontalface_alt_tree.xml')

face_cascade.load('./123/data/haarcascade_frontalface_alt_tree.xml')



app = Flask(__name__)

#進入圖像辨識模式的開關
switch = False


#辨識func
def readheadshot(photo):
    '''

    :param photo: input binary of pic
    :return: output string
    '''

    arr  = np.asarray(bytearray(photo), dtype=np.uint8)

    img  = cv2.imdecode(arr, -1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #轉灰階
    
    # 偵測臉部
    faces = face_cascade.detectMultiScale( 
        gray,
        scaleFactor=1.01,
        minNeighbors=5,
        minSize=(32, 32))

    if len(faces) >1:
        return "您好!您上傳的照片中偵測到多個人像,做為求職大頭照較不適當,如果可以請重新上傳,謝謝。"
    elif  len(faces) == 0 :
        return "您好!您上傳的照片內,並無人像,做為求職大頭照較不適當,如果可以請重新上傳,謝謝。"
    else:
        return readheadshots(photo)


@app.route("/", methods=['POST'])
def callback():

    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


Followeventmessage='''歡迎使用  "勇往職前" : AI求職招聘媒合助理-聊天機器人

以下為四大功能介紹 : 

1. 找職缺 

 • 求職者輸入想要的工作條件，履歷表，自傳 → 推薦10筆適合的的職缺。

2. 找履歷 

 •  人資輸入招聘內容與條件 →推薦Cake Resume 的履歷表。

3. 求職大頭照辨識 

 •  利用AI影像辨識照片是否適合當求職用大頭照。

4. 職缺分析報表 

 •  分析當前台灣招聘市場，產生Tableau報表(dashboard)。
'''


from linebot.models.events import FollowEvent
@handler.add(FollowEvent)
def reply_text_and_get_user_profile(event):
    # 取出消息內User的資料
    line_bot_api.link_rich_menu_to_user(event.source.user_id,"richmenu-7dcf3fe981784603bab6653fcb72a628")
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=Followeventmessage)
    )

@handler.add(MessageEvent, message=ImageMessage)
def handle_message(event):
    global switch
    if switch :
        message_content = line_bot_api.get_message_content(event.message.id)
        print(message_content.content)
        path= './'+event.message.id+'.jpg'

        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=readheadshot(message_content.content))
        )
        switch = False
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請點擊下方查看更多資訊->頭像辨識按鈕之後再上傳圖片")
        )

from linebot.models import PostbackEvent
@handler.add(PostbackEvent)
def handle_post_message(event):
    global switch
    if event.postback.data == "headshot":
        switch = True

if __name__ == "__main__":

    app.run(host='0.0.0.0')

    #Use for heroku
    #app.run(host='0.0.0.0', port=os.environ['PORT'])
