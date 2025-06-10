import requests
import os

def get_price():
    url = "https://api.velodrome.finance/api/v1/pairs"
    res = requests.get(url).json()
    for pool in res["data"]:
        if pool["name"] == "USDC/OP":
            return float(pool["price_usd"])
    return None

def send_line_notify(message, token):
    headers = {"Authorization": f"Bearer {token}"}
    data = {"message": message}
    requests.post("https://notify-api.line.me/api/notify", headers=headers, data=data)

if __name__ == "__main__":
    price = get_price()
    low = 1.10
    high = 1.30
    token = os.environ.get("LINE_NOTIFY_TOKEN")

    if price is None:
        send_line_notify("⚠️ Velodrome価格取得失敗", token)
    elif not (low <= price <= high):
        send_line_notify(f"⚠️ レンジ外: 現在価格は {price}", token)
