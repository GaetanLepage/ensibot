#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    EnsiBot main class
"""

import os
import time
import random as rd

# TODO remove when io_api will be an external software
from io_api.io_api import IoApi

# from ui.ensibot_ui_interface import EnsibotUiInterface


# Loggers
import logging.handlers

PYTHON_LOGGER = logging.getLogger("EnsiBot")
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/ensibot_model.log", when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

class Ensibot():
    """
    Implementation of the decision engine
    """

    def __init__(self, enable_ui):

        self.screen_res_width = 1024
        self.screen_res_height = 768

        self.io_api = IoApi()

        if enable_ui:
            # self.ui = EnsibotUiInterface()
            pass

    def run(self):
        """
        Runs the model in testing mode (no learning)
        """
        while True:
            # Get Image
            # TODO

            # Compute X,Y
            x, y = rd.randint(0, self.screen_res_width), rd.randint(0, self.screen_res_height)

            # Send X,Y to IO API
            self.io_api.send_mouse_event(
                coord_x=x,
                coord_y=y)

            time.sleep(2)
