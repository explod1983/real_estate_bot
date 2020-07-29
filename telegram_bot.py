# -*- coding: utf-8 -*-
import config
import telebot
from site_parser import Parser, compare_results_with_db
import time
from _datetime import datetime
import sys
import os


bot = telebot.TeleBot(config.token)
date = datetime.now().strftime("%d %B, %Y")

DIR_PATH = os.path.dirname(os.path.realpath(__file__))

URL_SVENSKA = 'https://www.svenskfast.se'
URL_SVENSKA_ALE = f'{URL_SVENSKA}/hus/vastra-gotaland/ale/'
FILE_SVENSKA = 'svenskfast_base.txt'
SVENSKA_DB_BASE_PATH = f'{DIR_PATH}/base/{FILE_SVENSKA}'

URL_ERA = 'https://www.erasweden.com'
URL_ERA_ALE = f'{URL_ERA}/hitta-din-bostad?query=Commune%3A%22Ale%22'
FILE_ERA = 'era_base.txt'
ERA_DB_BASE_PATH = f'{DIR_PATH}/base/{FILE_ERA}'

era_parser = Parser(URL_ERA_ALE)
era_results = era_parser.era_filter(URL_ERA)
svenska_parser = Parser(URL_SVENSKA_ALE)
svenska_results = svenska_parser.svenska_filter(URL_SVENSKA)


@bot.message_handler(content_types=["text"])
def send_respond(message):
    while True:
        try:
            updates = compare_results_with_db(era_results, era_parser.read_db(ERA_DB_BASE_PATH))
            if len(updates) > 0:
                bot.send_message(message.chat.id, f'ERA New houses: for {date}')
                for era_house in updates:
                    bot.send_message(message.chat.id, era_house)
            era_parser.update_db(era_results, ERA_DB_BASE_PATH)
        except:
            e = sys.exc_info()[0]
            bot.send_message(message.chat.id, f"ERA request went wrong:\n {e}")

        try:
            updates_svenska = compare_results_with_db(svenska_results, svenska_parser.read_db(SVENSKA_DB_BASE_PATH))
            if len(updates_svenska) > 0:
                bot.send_message(message.chat.id, f'Svenska New houses: for {date}')
                for svenska_house in updates_svenska:
                    bot.send_message(message.chat.id, svenska_house)
            svenska_parser.update_db(svenska_results, SVENSKA_DB_BASE_PATH)
            time.sleep(60)
        except:
            e = sys.exc_info()[0]
            bot.send_message(message.chat.id, f"Svenska Fast went wrong\n {e}")
        time.sleep(60)


if __name__ == '__main__':
     bot.polling(none_stop=True)
