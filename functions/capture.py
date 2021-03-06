import numpy as np
import os

from threading import Lock, Thread
from mss import mss
from time import time


class WindowCapture:

    # properties
    stopped = True
    lock = None
    screenshot = None
    w = 0
    h = 0
    cropped_x = 0
    cropped_y = 0
    offset_x = 0
    offset_y = 0
    buff_bar_pos = (0, 0)
    fps = 1
    screen = mss()
    region = None

    def __init__(self, border_pixels, titlebar_pixels):
        self.lock = Lock()

        window_rect = [0, 0, 0, 0]

        data = os.popen('wmctrl -lG | grep "Lineage II"').read()
        variables = data.split()
        window_rect[0] = int(variables[2])
        window_rect[1] = int(variables[3])
        window_rect[2] = int(variables[4])
        window_rect[3] = int(variables[5])

        self.offset_x = window_rect[0]
        self.offset_y = window_rect[1]

        self.cropped_x = border_pixels + self.offset_x
        self.cropped_y = titlebar_pixels + self.offset_y

        self.w = window_rect[2]
        self.h = window_rect[3]
        self.region = {'top': self.offset_y, 'left': self.offset_x,
                       'width': self.w - 50, 'height': self.h - 50}

    def set_buff_bar_pos(self, buff_bar_pos):
        self.buff_bar_pos = buff_bar_pos

    def get_screenshot(self):
        img = np.array(self.screen.grab(self.region))
        # hide buff bar
        # (y:h+y, x:w+x)
        img[int(self.buff_bar_pos[1]):105 + int(self.buff_bar_pos[1]),
            int(self.buff_bar_pos[0]):325 + int(self.buff_bar_pos[0])] = (0, 0, 0, 0)
        return img

    def start(self):
        self.stopped = False
        t = Thread(target=self.run)
        t.start()

    def stop(self):
        self.stopped = True

    def run(self):
        while not self.stopped:
            start = time()
            screenshot = self.get_screenshot()
            with self.lock:
                self.screenshot = screenshot
            self.fps = round(1.0 / (time() - start), 1)
