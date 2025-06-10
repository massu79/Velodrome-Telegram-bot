import requests
import os

def _get_price():
    url = "https://api.velodrome.finance/api/v1/pairs"
    res = requests.get(url).json()
    for pool in res["data"]:
        if pool["name"] == "USDC/OP":
            return float(pool["price_usd"])
    return None

def get_price():
    url = "https://api.coingecko.com/api/v3/simple/price?ids=optimism&vs_currencies=usd"
    res = requests.get(url).json()
    return res["optimism"]["usd"]

def send_telegram(message):
    token = os.environ["BOT_TOKEN"]
    chat_id = os.environ["CHAT_ID"]
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

if __name__ == "__main__":
    price = get_price()
    low = 1.10
    high = 1.30

    if price is None:
        send_telegram("⚠️ Velodrome価格取得失敗")
    elif not (low <= price <= high):
        send_telegram(f"⚠️ レンジ外: 現在価格は {price}")
