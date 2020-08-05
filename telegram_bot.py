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


@bot.message_handler(commands=['new_houses'])
def new_houses(message):
    try:
        for site in web_sites:
            site_parser = Parser(site['URL'])
            db_file_path = DIR_PATH + site['PATH']
            site_results = site_parser.main_filter()
            updates = compare_results_with_db(site_results, site_parser.read_db(db_file_path))
            if len(updates) > 0:
                bot.send_message(message.chat.id, '{}\n New houses: for {}'.format(date, site['URL'].split('/')[2]))
                for new_house in updates:
                    bot.send_message(message.chat.id, new_house)
            else:
                bot.send_message(message.chat.id, 'No new homes for {}'.format(site['URL'].split('/')[2]))
            site_parser.update_db(site_results, db_file_path)
    except:
        e = sys.exc_info()
        bot.send_message(message.chat.id, f"Bot is broken:\n {e}")


@bot.message_handler(commands=['all_houses'])
def all_houses(message):
    try:
        for site in web_sites:
            site_parser = Parser(site['URL'])
            site_results = site_parser.main_filter()
            bot.send_message(message.chat.id, '{}\n New houses: for {}'.format(date, site['URL'].split('/')[2]))
            for new_house in site_results:
                bot.send_message(message.chat.id, new_house)
    except:
        e = sys.exc_info()
        bot.send_message(message.chat.id, f"Bot is broken:\n {e}")


@bot.message_handler(commands=['skepplanda'])
def all_houses(message):
    try:
        for site in web_sites:
            site_parser = Parser(site['URL'])
            site_results = site_parser.main_filter()
            bot.send_message(message.chat.id, '{}\n New houses: for {}'.format(date, site['URL'].split('/')[2]))
            for new_house in site_results:
                bot.send_message(message.chat.id, new_house)
    except:
        e = sys.exc_info()
        bot.send_message(message.chat.id, f"Bot is broken:\n {e}")


@bot.message_handler(commands=['alive'])
def send_respond(message):
    bot.send_message(message.chat.id, f"I'm alive")


if __name__ == '__main__':
     bot.polling(none_stop=True, timeout=60)
