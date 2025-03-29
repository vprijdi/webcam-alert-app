import requests
import os


def send_telegram_alert(photo_location):
    # Telegram bot token
    token = os.getenv("WEBCAM_ALERT_BOT_TOKEN")
    # Telegram chat id
    chat_id = os.getenv("WEBCAM_ALERT_BOT_CHATID")

    url = f'https://api.telegram.org/bot{token}/sendPhoto'
    photo = open(photo_location, 'rb')

    data = {
        'chat_id': chat_id,
        'caption': "New object detected on camera"
    }
    files = {
        'photo': photo
    }

    response = requests.post(url, data=data, files=files)


if __name__ == "__main__":
    send_telegram_alert("images\\image1.png")
