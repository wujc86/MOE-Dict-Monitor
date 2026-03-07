import requests
import json
from datetime import datetime
import pytz

# 定義監控目標 (教育部五大辭典)
targets = {
    "重編國語辭典修訂本": "https://dict.revised.moe.edu.tw/",
    "國語辭典修訂本": "https://dict.concise.moe.edu.tw/",
    "國語小字典": "https://dict.mini.moe.edu.tw/",
    "成語典": "https://dict.idioms.moe.edu.tw/",
    "異體字字典": "https://dict.variants.moe.edu.tw/"
}

results = []
# 設定時區為台北
tw_tz = pytz.timezone('Asia/Taipei')
now = datetime.now(tw_tz).strftime("%Y-%m-%d %H:%M:%S")

for name, url in targets.items():
    try:
        # 使用 HEAD 請求快速檢查狀態碼
        res = requests.head(url, timeout=15, allow_redirects=True)
        status = "Online" if res.status_code == 200 else f"Error({res.status_code})"
    except Exception as e:
        status = "Offline"
    
    results.append({
        "name": name,
        "url": url,
        "status": status
    })

# 存成 JSON 檔供前端網頁讀取
output_data = {
    "last_update": now,
    "results": results
}

with open("status.json", "w", encoding="utf-8") as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print(f"Update successful at {now}")
