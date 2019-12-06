#!/usr/bin/env python3

import socket
import threading
import struct
import time
import os

# Loggers
import logging.handlers

PYTHON_LOGGER = logging.getLogger("SocketClient")
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler(
    "log/socket_client.log",
    when="midnight",
    backupCount=60)
FORMATTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HANDLER = logging.StreamHandler()
STREAM_HANDLER.setLevel(logging.INFO)
STREAM_HANDLER.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HANDLER)
PYTHON_LOGGER.setLevel(logging.DEBUG)


class SocketClient(threading.Thread):
    """
    Assure the connection to the CSGO reward API thanks to a socket.
    This class is inheriting from a thread to be executed externally from the EnsiBot model.
    """

    def __init__(self, server_ip, server_port):

        threading.Thread.__init__(self)

        self.server_ip = server_ip
        self.server_port = server_port

        self.socket = None
        self.is_connected = False

    def connect_to_server(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.socket.setblocking(False)
        self.socket.connect((self.server_ip, self.server_port))
        self.is_connected = True
    
    def run(self):
        self.connect_to_server()
        print("Connected to server")
        while True:
            time.sleep(1)

    def send_string_message(self, string_message):
        """
        """
        if not self.is_connected:
            return False

        if string_message[-1] != '\0':
            string_message += '\0'
        message_bytes = string_message.encode()
        self.socket.sendall(message_bytes)
        # print("sent message \"{}\"".format(string_message))

        return True
    
    def receive_float(self):
        bufsize=4
        float_bytes = self.socket.recv(bufsize)

        res = struct.unpack('f', float_bytes)

        return res[0]