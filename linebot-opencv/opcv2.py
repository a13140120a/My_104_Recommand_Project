import cv2
import glob
import numpy as np
# 載入分類器
face_cascade = cv2.CascadeClassifier('./123/data/haarcascade_fullbody.xml')
face_cascade.load('./123/data/haarcascade_fullbody.xml')

# #路徑版本
# def readheadshots(photo):
#
#     img = cv2.imread(photo)
#     #轉灰階
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#     # 偵測臉部
#     faces = face_cascade.detectMultiScale(
#         gray,
#         scaleFactor=1.01,
#         minNeighbors=5,
#         minSize=(32, 32))
#     #print(len(faces))
#     #print(faces)
#     if len(faces) >1:
#         return "如果可以請放正式一點的照片"
#     else  :
#             return "祝你面試成功"


# binary版本
def readheadshots(photo):

    arr = np.asarray(bytearray(photo), dtype=np.uint8)

    img = cv2.imdecode(arr, -1)  # 'Load it as it is'
    #轉灰階
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 偵測臉部
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.01,
        minNeighbors=5,
        minSize=(32, 32))
    #print(len(faces))
    #print(faces)
    if len(faces) >2:
        return "您上傳的照片，服裝較不正式，做為求職大頭照，較不適當，如果可以，請重新上傳，謝謝!"
    else  :
        return "您好!您上傳的照片非常適合非常適合作為求職照,祝您求職順利"

