#!/usr/bin/env python3


# py dependencies
import os
import timeit

# pyqtgraph dependencies
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

# multithreading
from multiprocessing import Process
import queue


# Loggers
import logging.handlers

PYTHON_LOGGER = logging.getLogger("EnsiBotUiProcess")
if not os.path.exists("log"):
    os.mkdir("log")
HDLR = logging.handlers.TimedRotatingFileHandler(
    "log/ensibot_ui_process.log",
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


class EnsibotUiProcess(Process):

    def __init__(self, data_queue, command_queue):
        Process.__init__(self)
        self.data_queue = data_queue
        self.command_queue = command_queue

    def run(self):
        try:
            # setup interface objects
            self.setup_interface()

            # set Timer to update the interface regularly
            timer = QtCore.QTimer()
            timer.timeout.connect(lambda: self.update(self.data_queue))
            # updated every 1ms
            timer.start(1)

            # execute UI app (blocking)
            QtGui.QApplication.instance().exec_()

        except Exception as e:
            PYTHON_LOGGER.error("Exception on run: %s" % e)

        PYTHON_LOGGER.info("Interface has been closed")

    def setup_interface(self):
        """
            setup the objects for the interface
        """

        self.app = QtGui.QApplication([])

        ## VIDEO UI
        self.view_video = pg.GraphicsWindow()
        self.layout_video = pg.GraphicsLayout(border=(100, 100, 100))
        self.view_video.setCentralItem(self.layout_video)
        self.view_video.show()
        self.view_video.setWindowTitle('EnsiBot')
        self.view_video.resize(1400, 1000)

        # ################ ROW 0 ####################

        # self.header_layout = HeaderLayout(self.layout_video, self.command_queue, self.device_id)
        # self.layout_video.nextRow()

        # ################ ROW 1 ####################

        # self.input_layout = InputLayout(self.layout_video)

        # # computation times
        # self.computation_time_layout = self.layout_video.addLabel(self.get_computation_time_text())

        # self.layout_video.nextRow()
        # ################ ROW 2 ####################

        # self.attention_layout = AttentionLayout(self.layout_video)
        # self.layout_video.nextRow()


    def update(self, input_queue):
        """
            update UI method called every X ms
            reads the queue and updates the interface

            **input:**
                * queue (Queue): queue containing the data of the perception algorithms
        """
        try:
            input_data = input_queue.get(False)
        except queue.Empty:
            # queue empty, exception raised
            # so the update method is not blocked and doesn't freeze the UI
            return

        # input_queue is a tuple of form (<topic>, <payload>)
        topic = input_data[0]
        payload = input_data[1]

        # get starting time to compute the refreshing time
        start_time = timeit.default_timer()

        # if topic == PerceptionTopics.INPUT_CONFIG.value.format(self.device_id):
        #     self.input_layout.update_config(json.loads(payload))
        # elif topic == PerceptionTopics.INPUT_RAW.value.format(self.device_id):
        #     self.input_layout.update_frame(payload)
        # elif topic == PerceptionTopics.FACIAL_LANDMARKS.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.input_layout.draw_facial_landmarks(payload['features'])
        #     self.facial_landmarks_computation_time = payload['computation_time']
        # elif topic == PerceptionTopics.ATTENTION.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.attention_layout.update(payload)
        #     self.attention_computation_time = payload['direct_visual_attention']['computation_time']
        # elif topic == PerceptionTopics.ENGAGEMENT.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.engagement_layout.update(payload)
        #     self.engagement_computation_time = payload['computation_time']
        # elif topic == PerceptionTopics.FACE_RECOGNITION.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.input_layout.draw_faces(payload['users'])
        #     self.face_recognition_computation_time = payload['computation_time']
        # elif topic == PerceptionTopics.YOLO.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.input_layout.draw_objects(payload['yolo_prediction'])
        #     self.yolo_computation_time = payload['computation_time']
        # elif topic == PerceptionTopics.INTERACTING_USER.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.input_layout.update_interacting_user(payload)
        # elif topic == PerceptionTopics.STATUS_FRAME_COLLECTION.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.header_layout.set_collect_status(payload)
        # elif topic == PerceptionTopics.OPEN_FACE.value.format(self.device_id):
        #     payload = json.loads(payload)

        #     # display open face head pose and landarks
        #     self.input_layout.draw_open_face(payload)

        #     # display action units values
        #     self.action_units_layout.update(payload['action_units'])

        #     # update open face computation_time
        #     if 'computation_time' in payload:
        #         self.open_face_computation_time = payload['computation_time']
        # elif topic == PerceptionTopics.PROXEMICS.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.proxemics_layout.update(payload)
        # elif topic == PerceptionTopics.FACIAL_EMOTIONS.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.emotions_layout.update(payload)

        # # Audio messages
        # # If the audio UI is disabled, the engine_interface_node will not
        # # subscribe to the audio topics and those line won't be used
        # elif topic == PerceptionTopics.INPUT_CONFIG_AUDIO.value.format(self.device_id):
        #     self.audio_input_layout.update_config(json.loads(payload))
        # elif topic == PerceptionTopics.INPUT_RAW_AUDIO.value.format(self.device_id):
        #     self.audio_input_layout.update_signal(payload)
        # elif topic == PerceptionTopics.STATUS_AUDIO_COLLECTION.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.audio_header_layout.set_collect_status(payload)
        # elif topic == PerceptionTopics.MFCC.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.audio_features_layout.update_mfcc(payload)
        # elif topic == PerceptionTopics.AUDIO_FEATURES.value.format(self.device_id):
        #     payload = json.loads(payload)
        #     self.audio_features_layout.update_features(payload)

        # # update computation times
        # try:
        #     self.computation_time_layout.setText(self.get_computation_time_text())
        # except Exception as e:
        #     PYTHON_LOGGER.warning("Exception while updating computation times: %s", e)

        # refresh_ui_time = timeit.default_timer() - start_time
        # self.header_layout.update(refresh_ui_time)
