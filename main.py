#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import time

API_URL = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
API_KEY = "CWA-738C42B9-49B2-412C-BD7C-080975813398"
WEBHOOK_URL = "https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af"

last_eq_id = None  # 儲存上次處理的地震 ID，防止重複處理

def fetch_latest_earthquake():
    global last_eq_id

    try:
        # 訪問 API 獲取資料
        response = requests.get(API_URL, params={"Authorization": API_KEY})
        data = response.json()

        # 打印出 API 返回的資料結構
        print("API 返回資料：", data)

        # 檢查資料格式是否正確
        if "records" in data and "earthquake" in data["records"]:
            earthquake_data = data["records"]["earthquake"]
            
            # 如果沒有新的地震資料
            if not earthquake_data:
                print("目前無地震資料")
                return
            
            # 處理每一筆地震資料
            for eq in earthquake_data:
                eq_id = eq.get('earthquakeID')

                # 檢查是否已經處理過此地震
                if eq_id != last_eq_id:
                    # 更新 last_eq_id 為當前地震 ID
                    last_eq_id = eq_id
                    
                    # 構建 Webhook 要發送的訊息
                    message = {
                        "title": "新地震資料",
                        "content": f"地震編號: {eq['earthquakeID']}\n震中: {eq['epicenter']}\n震度: {eq['magnitude']}\n時間: {eq['earthquakeTime']}"
                    }
                    
                    # 發送 Webhook 通知
                    send_webhook(message)
                    
                    # 輸出處理過的地震資料
                    print(f"處理新地震資料：{eq}")

        else:
            print("API 返回的資料格式異常或無地震資料")
    
    except Exception as e:
        print("抓取地震資料時發生錯誤：", e)

def send_webhook(message):
    try:
        # 發送 POST 請求到 Webhook
        response = requests.post(WEBHOOK_URL, json=message)
        if response.status_code == 200:
            print("Webhook 發送成功")
        else:
            print(f"Webhook 發送失敗，狀態碼：{response.status_code}")
    except Exception as e:
        print("發送 Webhook 時發生錯誤：", e)

# 持續每60秒檢查一次地震資料
while True:
    fetch_latest_earthquake()
    time.sleep(60)  # 每60秒抓取一次


# In[ ]:




