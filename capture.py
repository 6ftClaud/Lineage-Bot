from threading import Thread, Lock
from PIL import ImageGrab
import numpy as np
import os
import subprocess
import cv2 as cv

class WindowCapture:

	# output
	message = ''

	# properties
	stopped = True
	lock = None
	screenshot = None
	w = 0
	h = 0
	hwnd = None
	cropped_x = 0
	cropped_y = 0
	offset_x = 0
	offset_y = 0
	debug = None
	buff_bar_pos = (0, 0)

	def __init__(self, border_pixels, titlebar_pixels):
		self.lock = Lock()

		window_rect = [0, 0, 0, 0]

		data = os.popen('wmctrl -lG | grep "Lineage II"').read()
		variables = data.split()
		window_rect[0] = int(float(variables[2]))
		window_rect[1] = int(float(variables[3]))
		window_rect[2] = int(float(variables[4]))
		window_rect[3] = int(float(variables[5]))

	

		self.cropped_x = border_pixels + self.offset_x
		self.cropped_y = titlebar_pixels + self.offset_y

		self.offset_x = window_rect[0]
		self.offset_y = window_rect[1]

		self.w = window_rect[2] + self.offset_x
		self.h = window_rect[3] + self.offset_y


	def set_buff_bar_pos(self, buff_bar_pos):
		self.buff_bar_pos = buff_bar_pos

	def get_screenshot(self):
		self.message = f"Capturing screen"
		img = ImageGrab.grab(bbox=(self.offset_x, self.offset_y, self.w - 45, self.h))
		img = np.array(img)
		# hide buff bar
		# (y:h+y, x:w+x)
		img[int(self.buff_bar_pos[1]):105 + int(self.buff_bar_pos[1]), int(self.buff_bar_pos[0]):325 + int(self.buff_bar_pos[0])] = (0, 0, 0)
		return img

	# gets X and Y coordinates of enemies
	def get_enemy_coordinates(self):
		self.message = f"Getting enemy coordinates"
		# converting screen to grayscale
		screen = cv.cvtColor(self.screenshot, cv.COLOR_BGR2GRAY)
		# finding white text (enemies)
		ret, enemies = cv.threshold(screen, 252, 255, cv.THRESH_BINARY)
		# forms a white bar in order to get the X and Y coordinates with the findContours and rectangle cv functions
		kernel = cv.getStructuringElement(cv.MORPH_RECT, (50, 5))
		enemies = cv.morphologyEx(enemies, cv.MORPH_CLOSE, kernel)
		#enemies = cv.erode(enemies, kernel, iterations=1)
		#enemies = cv.dilate(enemies, kernel, iterations=1)
		(contours, hierarchy) = cv.findContours(enemies, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
		# extracting enemy x and y coordinates from contours
		targets = []
		for c in contours:
			if cv.contourArea(c) > 20:
				x, y, w, h = cv.boundingRect(c)
				target = ((x + w / 2), (y + h / 2) + 35)
				targets.append(target)
		return targets


	def start(self):
		self.stopped = False
		t = Thread(target=self.run)
		t.start()

	def stop(self):
		self.stopped = True

	def run(self):
		while not self.stopped:
			screenshot = self.get_screenshot()
			self.lock.acquire()
			self.screenshot = screenshot
			self.lock.release()