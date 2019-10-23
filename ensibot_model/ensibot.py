#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    EnsiBot main class
"""

import os

# TODO remove when io_api will be an external software
from io_api.io_api import IoApi

from ui.ensibot_ui_interface import EnsibotUiInterface


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
    """

    def __init__(self, enable_ui):
        
        if enable_ui:
            self.ui = EnsibotUiInterface()
