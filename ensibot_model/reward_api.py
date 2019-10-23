#!/usr/bin/env python3

"""
Connector to the Ensibot C++ reward API which is being injected in CSGO
"""

import time
import struct
import os
from socket_client import SocketClient

# Loggers
import logging.handlers

PYTHON_LOGGER = logging.getLogger("RewardApi")
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler(
    "log/reward_api.log",
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

# HOST = '127.0.0.1'
# HOST = '192.168.1.24'
HOST = 'localhost'
PORT = 3121

class RewardApi():
    
    def __init__(self):
        """
        Constructor for the RewardApi class
        """
        self.socket_client = SocketClient(HOST, PORT)
        self.socket_client.start()

    def get_reward(self):
        """
        Send the 'get_reward' command to the socket server (CSGO reward API)
        Wait for the response and return the reward value

        **output**:
            * None if the socket connection is not valid
            * reward (float) : the reward value
        """
        if not self.socket_client.send_string_message("get_reward"):
            # TODO : raise exception + logging
            return

        return self.socket_client.receive_float()

def main():
    # TODO remove (this was just for testing purposes)
    reward_api = RewardApi()

    print("init over")

    while True:
        if reward_api.socket_client.is_connected:
            reward = reward_api.get_reward()
            print(reward)

        time.sleep(0.1)


if __name__=="__main__":
    main()
