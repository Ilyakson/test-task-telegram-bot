import os

from bs4 import BeautifulSoup
import telebot
import requests

import random

bot = telebot.TeleBot(os.getenv("BOT_KEY"))
URL = "https://paper-trader.frwd.one"
deadline_list = ["5m", "15m", "1h", "4h", "1d", "1w", "1M"]
crypto_pair = ["BNBUSDT", "ETHUSDT", "BTCUSDT"]


def validate_message(message):
    if message.text in crypto_pair:
        return True
    else:
        return False


def get_image(message):
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


@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(
        message.chat.id,
        f"<b>Hello, pick the trading pair, current pair: {crypto_pair}</b>",
        parse_mode="html"
    )


@bot.message_handler()
def send_image(message):
    if validate_message(message):
        bot.send_photo(message.chat.id, f"{URL}{get_image(message)}")
    else:
        bot.send_message(
            message.chat.id,
            f"<b>Please input correct value of trading pair, to see all current pairs input /start</b>",
            parse_mode="html"
        )


bot.polling(none_stop=True)
