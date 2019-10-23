#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TODO doc
"""

import os
import pyautogui

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

class IoApi():
    """
    TODO doc
    """

    def __init__(self):
        pass

    def get_frame(self):
        pass

    def send_mouse_event(self, coord_x, coord_y):
        pyautogui.click(
            x=coord_x,
            y=coord_y
        )
        pass
