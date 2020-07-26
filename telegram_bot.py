# -*- coding: utf-8 -*-
import config
import telebot
from parse_era import update_era_db, compare_ERA_latest_with_db
from parse_svenskfast import update_SVENSKAFAST_db, compare_SVENSKAFAST_latest_with_db
import time
from _datetime import datetime

bot = telebot.TeleBot(config.token)
date = datetime.now().strftime("%d %B, %Y")


@bot.message_handler(content_types=["text"])
def send_respond(message):
    while True:
        try:
            if len(compare_ERA_latest_with_db()) > 0:
                bot.send_message(message.chat.id, f'ERA New houses: for {date}')
                for era_house in compare_ERA_latest_with_db():
                    bot.send_message(message.chat.id, era_house)
            update_era_db()
        except:
            bot.send_message(message.chat.id, "ERA request went wrong")

        try:
            if len(compare_SVENSKAFAST_latest_with_db()) > 0:
                bot.send_message(message.chat.id, f'Svenska Fast New houses: for {date}')
                for svenska_house in compare_SVENSKAFAST_latest_with_db():
                    bot.send_message(message.chat.id, svenska_house)
            update_SVENSKAFAST_db()
            time.sleep(60)
        except:
            bot.send_message(message.chat.id, "Svenska Fast went wrong")


if __name__ == '__main__':
     bot.polling(none_stop=True)
