import os
import requests
import time
from datetime import datetime

# Sửa phần này thành dùng biến môi trường
CRYPTO_PANIC_API_KEY = os.getenv('CRYPTO_PANIC_API_KEY')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHANNEL_ID = os.getenv('TELEGRAM_CHANNEL_ID')  # Hoặc chat ID (-12345678)

def get_crypto_news():
    url = f"https://cryptopanic.com/api/v1/posts/?auth_token={CRYPTO_PANIC_API_KEY}&currencies=BTC,ETH"
    
    try:
        response = requests.get(url)
        data = response.json()
        return data['results']
    except Exception as e:
        print(f"Error fetching news: {e}")
        return []

def send_to_telegram(message):
    telegram_api = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        'chat_id': TELEGRAM_CHANNEL_ID,
        'text': message,
        'parse_mode': 'HTML'
    }
    requests.post(telegram_api, data=payload)

def format_news(news):
    message = f"<b>{news['title']}</b>\n"
    message += f"📰 Source: {news['source']['title']}\n"
    message += f"⏰ Published: {news['published_at']}\n"
    message += f"🔗 Link: {news['url']}"
    return message

def main():
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    print(f"Checking news at {now}...")

    news_items = get_crypto_news()

    for item in news_items[:2]:  # Gửi 2 tin mới nhất
        news_message = format_news(item)
        send_to_telegram(news_message)

if __name__ == "__main__":
    main()
