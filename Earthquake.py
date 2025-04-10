{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "ename": "KeyError",
     "evalue": "'earthquake'",
     "output_type": "error",
     "traceback": [
      "\u001b[0;31m---------------------------------------------------------------------------\u001b[0m",
      "\u001b[0;31mKeyError\u001b[0m                                  Traceback (most recent call last)",
      "Cell \u001b[0;32mIn[2], line 45\u001b[0m\n\u001b[1;32m     42\u001b[0m         \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m無新地震，等待中...\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[1;32m     44\u001b[0m \u001b[38;5;28;01mwhile\u001b[39;00m \u001b[38;5;28;01mTrue\u001b[39;00m:\n\u001b[0;32m---> 45\u001b[0m     \u001b[43mfetch_latest_earthquake\u001b[49m\u001b[43m(\u001b[49m\u001b[43m)\u001b[49m\n\u001b[1;32m     46\u001b[0m     time\u001b[38;5;241m.\u001b[39msleep(\u001b[38;5;241m60\u001b[39m)  \u001b[38;5;66;03m# 每60秒抓一次\u001b[39;00m\n",
      "Cell \u001b[0;32mIn[2], line 15\u001b[0m, in \u001b[0;36mfetch_latest_earthquake\u001b[0;34m()\u001b[0m\n\u001b[1;32m     12\u001b[0m response \u001b[38;5;241m=\u001b[39m requests\u001b[38;5;241m.\u001b[39mget(API_URL, params\u001b[38;5;241m=\u001b[39m{\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124mAuthorization\u001b[39m\u001b[38;5;124m\"\u001b[39m: API_KEY})\n\u001b[1;32m     13\u001b[0m data \u001b[38;5;241m=\u001b[39m response\u001b[38;5;241m.\u001b[39mjson()\n\u001b[0;32m---> 15\u001b[0m \u001b[38;5;28;01mif\u001b[39;00m \u001b[38;5;129;01mnot\u001b[39;00m \u001b[43mdata\u001b[49m\u001b[43m[\u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mrecords\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m]\u001b[49m\u001b[43m[\u001b[49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[38;5;124;43mearthquake\u001b[39;49m\u001b[38;5;124;43m\"\u001b[39;49m\u001b[43m]\u001b[49m:\n\u001b[1;32m     16\u001b[0m     \u001b[38;5;28mprint\u001b[39m(\u001b[38;5;124m\"\u001b[39m\u001b[38;5;124m目前無地震資料\u001b[39m\u001b[38;5;124m\"\u001b[39m)\n\u001b[1;32m     17\u001b[0m     \u001b[38;5;28;01mreturn\u001b[39;00m\n",
      "\u001b[0;31mKeyError\u001b[0m: 'earthquake'"
     ]
    }
   ],
   "source": [
    "import requests\n",
    "import time\n",
    "\n",
    "API_URL = \"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001\"\n",
    "API_KEY = \"CWA-738C42B9-49B2-412C-BD7C-080975813398\"\n",
    "WEBHOOK_URL = \"https://hook.eu2.make.com/wa0099sdc5iorkyfaf8yqhv84iab98af\"\n",
    "\n",
    "last_eq_id = None\n",
    "\n",
    "def fetch_latest_earthquake():\n",
    "    global last_eq_id\n",
    "    response = requests.get(API_URL, params={\"Authorization\": API_KEY})\n",
    "    data = response.json()\n",
    "\n",
    "    if not data[\"records\"][\"earthquake\"]:\n",
    "        print(\"目前無地震資料\")\n",
    "        return\n",
    "\n",
    "    eq = data[\"records\"][\"earthquake\"][0]\n",
    "    eq_id = eq[\"earthquakeNo\"]\n",
    "\n",
    "    if eq_id != last_eq_id:\n",
    "        last_eq_id = eq_id\n",
    "\n",
    "        eq_time = eq[\"earthquakeInfo\"][\"originTime\"]\n",
    "        eq_location = eq[\"earthquakeInfo\"][\"epicenter\"][\"location\"]\n",
    "        eq_magnitude = eq[\"earthquakeInfo\"][\"magnitude\"][\"magnitudeValue\"]\n",
    "        eq_depth = eq[\"earthquakeInfo\"][\"depth\"][\"value\"]\n",
    "        eq_area = eq[\"intensity\"][\"shakingArea\"][0][\"areaDesc\"]\n",
    "\n",
    "        message = (\n",
    "            f\"【地震速報】\\n\"\n",
    "            f\"時間：{eq_time}\\n\"\n",
    "            f\"位置：{eq_location}\\n\"\n",
    "            f\"芮氏規模：{eq_magnitude}  深度：{eq_depth} km\\n\"\n",
    "            f\"影響地區：{eq_area}\"\n",
    "        )\n",
    "\n",
    "        print(\"發送貼文內容：\\n\" + message)\n",
    "        requests.post(WEBHOOK_URL, json={\"text\": message})\n",
    "    else:\n",
    "        print(\"無新地震，等待中...\")\n",
    "\n",
    "while True:\n",
    "    fetch_latest_earthquake()\n",
    "    time.sleep(60)  # 每60秒抓一次"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.11.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
