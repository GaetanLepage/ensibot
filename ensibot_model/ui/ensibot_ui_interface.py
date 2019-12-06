#!/usr/bin/env python3

# py dependencies
import os
import timeit

# pyqtgraph dependencies
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

# multithreading
import multiprocessing
from multiprocessing import Process, Queue

from ensibot_model.ui.ensibot_ui_process import EnsibotUiProcess


# Loggers
import logging.handlers

PYTHON_LOGGER = logging.getLogger("EnsiBotUiInterface")
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler(
    "log/ensibot_ui_interface.log",
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

class EnsibotUiInterface():

    def __init__(self):
        # queue to push data to the EnsibotUiProcess
        self.data_queue = multiprocessing.Queue()
        # queue to read commands from the interface
        self.command_queue = multiprocessing.Queue()

        self.start_ui_process()
    
    def start_ui_process(self):
        """
            Start the process holding the interface
        """
        # instanciate UI process
        self.interface_process = EnsibotUiProcess(self.data_queue, self.command_queue)
        self.interface_process.start()
    
    # TODO api functions (push new data...)

    def clean(self):
        """
            terminate the engine interface process
        """
        self.interface_process.terminate()