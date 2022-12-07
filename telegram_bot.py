import os

from bs4 import BeautifulSoup
import telebot
import requests

import random

BOT = telebot.TeleBot(os.getenv("BOT_KEY"))
URL = "https://paper-trader.frwd.one"
deadline_list = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]


def work_with_site(message):
    payload = {
        "pair": message.text,
        "timeframe": deadline_list[random.randint(0, 6)],
        "candles": random.randint(1, 1000),
        "ma": random.randint(1, 50),
        "tp": random.randint(1, 50),
        "sl": random.randint(1, 50),
    }
    response = requests.post(URL, data=payload)
    soup = BeautifulSoup(response.text, "html.parser")
    img = soup.find("img")
    image = img['src']
    return image[1:]


@BOT.message_handler(commands=["start"])
def start(message):
    BOT.send_message(
        message.chat.id,
        "<b>Hello, pick the trading pair (for example: BTCUSDT)</b>",
        parse_mode="html"
    )


@BOT.message_handler()
def sending_picture(message):
    BOT.send_photo(message.chat.id, f"{URL}{work_with_site(message)}")


BOT.polling(none_stop=True)
