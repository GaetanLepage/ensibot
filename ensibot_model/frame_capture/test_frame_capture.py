#!/usr/bin/env python


import time
import mss
import numpy as np
import cv2
from PIL import Image, ImageGrab


def screen_record():
    mon = {"top": 40, "left": 0, "width": 800, "height": 640}

    last_time = time.time()

    with mss.mss() as sct:

        while True:
            bgr_img = sct.grab(mon)
            np_img = np.asarray(bgr_img)

            rgb_img = Image.frombytes('RGB', bgr_img.size, bgr_img.bgra, 'raw', 'BGRX').tobytes()
            print("fps: {}".format(1 / (time.time() - last_time)))
            last_time = time.time()

            cv2.imshow("capture", np_img)
            if cv2.waitKey(25) & 0xFF == ord("q"):
                cv2.destroyAllWindows()
                return

screen_record()