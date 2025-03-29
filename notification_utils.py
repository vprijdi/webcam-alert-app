import requests
import os


def send_telegram_alert(photo_location):
    # Telegram bot token
    token = os.getenv("WEBCAM_ALERT_BOT_TOKEN")
    # Telegram chat id
    chat_id = os.getenv("WEBCAM_ALERT_BOT_CHATID")

    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    params = {
        'chat_id': chat_id,
        'photo': photo_location,
        'caption': "New object detected on camera"
    }

    response = requests.get(url, params=params)


if __name__ == "__main__":
    send_telegram_alert("https://picsum.photos/200/300")
