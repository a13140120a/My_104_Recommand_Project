FROM jjanzic/docker-python3-opencv

#設定一個工作資料夾
WORKDIR /app

#將本地的源碼複製進 Container的app資料夾
COPY . /app

#安裝套件
RUN pip install -r requirements.txt
#映射port
EXPOSE 5000

#較container預設執行app.py
CMD ["python", "app.py"]
