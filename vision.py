from threading import Thread, Lock
from PIL import ImageGrab
import numpy as np
import cv2 as cv
from time import time

class Vision:

	# properties
	screenshot = None
	targets = []
	fps=0

	def __init__(self, screenshot):
		self.lock = Lock()
		self.screenshot = screenshot

	# gets X and Y coordinates of enemies
	def get_enemy_coordinates(self):
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
				target = ((x + w / 2), (y + h / 2))
				targets.append(target)
		return targets

	def update_screenshot(self, screenshot):
		self.lock.acquire()
		self.screenshot = screenshot
		self.lock.release()

	def start(self):
		self.stopped = False
		t = Thread(target=self.run)
		t.start()

	def stop(self):
		self.stopped = True

	def run(self):
		while not self.stopped:
			start = time()
			targets = self.get_enemy_coordinates()
			self.targets = targets
			self.fps = round(1.0 / (time() - start), 1)
