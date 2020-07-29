# -*- coding: utf-8 -*-
import config
import telebot
from site_parser import Parser, compare_results_with_db
import time
from _datetime import datetime
import sys
from static_data import web_sites, DIR_PATH


bot = telebot.TeleBot(config.token)
date = datetime.now().strftime("%d %B, %Y")


@bot.message_handler(content_types=["text"])
def send_respond(message):
    while True:
        try:
            for site in web_sites:
                site_parser = Parser(site['URL'])
                db_file_path = DIR_PATH + site['PATH']
                site_results = site_parser.main_filter()
                updates = compare_results_with_db(site_results, site_parser.read_db(db_file_path))
                if len(updates) > 0:
                    bot.send_message(message.chat.id, '{}\n New houses: for {}'.format(date, site['URL'][12:25]))
                    for new_house in updates:
                        bot.send_message(message.chat.id, new_house)
                site_parser.update_db(site_results, db_file_path)
        except:
            e = sys.exc_info()[0]
            bot.send_message(message.chat.id, f"Bot is broken:\n {e}")

        time.sleep(60)


if __name__ == '__main__':
     bot.polling(none_stop=True)
