# -*- coding: utf-8 -*-
import config
import telebot
from parse_era import update_db, compare_latest_with_db
import time
from _datetime import datetime

bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def send_respond(message):
    while True:
        try:
            if len(compare_latest_with_db()) > 0:
                bot.send_message(message.chat.id, f' New houses: for {datetime.now().strftime("%d %B, %Y")}')
                for house in compare_latest_with_db():
                    bot.send_message(message.chat.id, house)
            update_db()
            time.sleep(60)
        except:
            bot.send_message(message.chat.id, "Something went wrong")


if __name__ == '__main__':
     bot.polling(none_stop=True)
