#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    EnsiBot Executable
"""

import argparse
# Loggers
import logging.handlers
import os

# from ui.ensibot_ui_interface import EnsibotUiInterface
from ensibot import Ensibot

PYTHON_LOGGER = logging.getLogger("EngineInterfaceExe")
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler("log/engine_interface_exe.log", when="midnight", backupCount=60)
STREAM_HDLR = logging.StreamHandler()
FORMATTER = logging.Formatter("%(asctime)s %(name)s [%(levelname)s] %(message)s")
HDLR.setFormatter(FORMATTER)
STREAM_HDLR.setFormatter(FORMATTER)
PYTHON_LOGGER.addHandler(HDLR)
PYTHON_LOGGER.addHandler(STREAM_HDLR)
PYTHON_LOGGER.setLevel(logging.DEBUG)

if __name__ == "__main__":
    # parse args
    parser = argparse.ArgumentParser(description='EngineInterface')
    parser.add_argument("--server-ip", dest="server_ip", default="localhost")
    parser.add_argument("--port", dest="server_port", default="1883")
    parser.add_argument("--ui", dest="enable_ui", default=False, type=bool)
    # modes
    parser.add_argument("--training", dest="training_mode", default=False, type=bool)
    parser.add_argument("--testing", dest="testing_mode", default=True, type=bool)
    args = parser.parse_args()

    PYTHON_LOGGER.info("Starting Ensibot")
    PYTHON_LOGGER.info(
        "Reward api host : IP=%s, PORT=%s",
        args.server_ip,
        args.server_port)

    ensibot = Ensibot(args.enable_ui)

    try:
        # start client
        # TODO maybe switch case training/test/demo/step by step ...
        if args.training_mode:
            pass
        elif args.testing_mode:
            ensibot.run()

        pass
    except Exception as e:
        PYTHON_LOGGER.error("Exception while running EngineInterfaceNode: %s", e)
        PYTHON_LOGGER.error("Is your ActiveMQ Broker running ?")
    finally:
        # properly stops ensibot
        # TODO : properly stop everything
        pass
