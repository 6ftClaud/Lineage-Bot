from PIL import Image, ImageGrab
from threading import Thread, Lock
import keyboard as keys
from pynput import keyboard
import pyautogui
import pytesseract
import cv2 as cv
import numpy as np
import os
import requests
from time import sleep, time


class Utils:

	# settings
	pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
	os.environ['TESSDATA_PREFIX'] = '/usr/share/tessdata'
	# output
	player_health = 100
	enemy_health = 0
	# properties
	screenshot = None
	timestamp = 0
	solving_captcha = False
	kbd = keyboard.Controller()

	max_player_health = 30.0 # px
	max_enemy_health = 30.0 # px
	current_player_health = 100 # %
	current_enemy_health = 100 # %

	player_hp_x_pos = 0
	player_hp_y_pos = 0
	player_hp_bar_width = 0
	player_hp_bar_height = 0
	enemy_hp_x_pos = 0
	enemy_hp_y_pos = 0
	enemy_hp_bar_width = 0
	enemy_hp_bar_height = 0
	buff_bar_pos = (0, 0)

	quest_window_x = 0
	quest_window_y = 0

	offset_x = 0
	offset_y = 0
	w = 0
	h = 0

	to_village_offset = 0
	fps = 1

	def __init__(self, offset_x, offset_y, w, h, UI_info, screenshot, to_village_offset):
		self.lock = Lock()

		self.timestamp = time()
		self.screenshot = screenshot

		self.to_village_offset = to_village_offset
		self.offset_x = offset_x
		self.offset_y = offset_y
		self.w = w
		self.h = h
		self.get_UI_positions(UI_info, offset_x, offset_y)

		self.farmingzones = (self.quest_window_x + 165), (self.quest_window_y + 203)
		self.dmg1 = (self.quest_window_x + 165), (self.quest_window_y + 234)

	def get_UI_positions(self, UI_info, offset_x, offset_y):
		lines = []
		with open(UI_info, 'r') as file:
			for line in file:
				if "=" in line:
					variable, value = line.split('=')
					lines.append(value)

		player_status = lines[16:18]
		self.player_hp_x_pos = int(player_status[0]) + 16
		self.player_hp_y_pos = int(player_status[1]) + 41
		self.player_hp_bar_width = 150
		self.player_hp_bar_height = 1

		enemy_status = lines[24:26]
		self.enemy_hp_x_pos = int(enemy_status[0]) + 16
		self.enemy_hp_y_pos = int(enemy_status[1]) + 28
		self.enemy_hp_bar_width = 150
		self.enemy_hp_bar_height = 1

		self.buff_bar_pos = (lines[40], lines[41])

		self.quest_window_x = int(lines[28]) + offset_x
		self.quest_window_y = int(lines[29]) + offset_y



	def player_health(self):
		y = self.player_hp_y_pos
		h = self.player_hp_bar_height + y
		x = self.player_hp_x_pos
		w = self.player_hp_bar_width + x
		im = self.screenshot[y:h, x:w]
		rgb = im[0]
		current_player_health = 0
		for r in range(0, len(rgb), 5):
			r = rgb[r][2]
			if r >= 214:
				current_player_health += 1.0
		percent_health = current_player_health * 100.0 / self.max_player_health
		percent_health = round(percent_health, 1)
		return percent_health

	def enemy_health(self):
		self.time = time()
		y = self.enemy_hp_y_pos
		h = self.enemy_hp_bar_height + y
		x = self.enemy_hp_x_pos
		w = self.enemy_hp_bar_width + x
		im = self.screenshot[y:h, x:w]
		rgb = im[0]
		current_enemy_health = 0
		for r in range(0, len(rgb), 5):
			r = rgb[r][2]
			if r == 214:
				current_enemy_health += 1.0
		enemy_percent_health = current_enemy_health * 100.0 / self.max_enemy_health
		enemy_percent_health = round(enemy_percent_health, 1)
		return enemy_percent_health

		# VEEEERY sketchy but that's the only way it works
	def target(self, text):
		try:
			keys.send('ENTER')
			self.kbd.type(text)
			keys.send('ENTER')
		except:
			raise Exception("Could not target successfully")

	def rebuff(self):
		self.message = f"Rebuffing"
		sleep(3)
		pyautogui.click((self.w / 2 + self.offset_x), (self.h / 2 + self.offset_y - self.to_village_offset))
		sleep(5)
		keys.send('F11')
		self.target("/target gatekeeper")
		self.target("/target gatekeeper")
		while not self.arrived_at_npc():
			sleep(0.01)
		pyautogui.click(self.farmingzones[0], self.farmingzones[1])
		sleep(0.5)
		pyautogui.click(self.dmg1[0], self.dmg1[1])
		return True

	def solve_captcha(self):
		x = self.quest_window_x + 52
		y = self.quest_window_y + 115
		w = 190
		h = 46
		api_key = 'd6aaaaa8d888957'
		payload = {'isOverlayRequired': False,
					   'apikey': api_key,
					   'OCREngine': 2,
					   'language': 'eng',}
		image = ImageGrab.grab(bbox=(x, y, w + x, h + y))
		image = np.array(image)
		image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
		image = cv.threshold(image, 0, 255, cv.THRESH_BINARY| cv.THRESH_OTSU)[1]
		image = cv.medianBlur(image, 1)
		BASE_DIR = os.path.dirname(os.path.abspath(__file__))
		f_path = BASE_DIR + "/img/captcha.png"
		cv.imwrite(f_path, image)
		with open(f_path, 'rb') as f:
			j = requests.post('https://api.ocr.space/parse/image', files={f_path: f}, data=payload).json()
			if j['ParsedResults']:
				result = j['ParsedResults'][0]['ParsedText']
		if '.' or ',' in result:
			result = result.replace('.','')
			result = result.replace(',','')
		pyautogui.click((x + w / 2), (y + 65))
		self.kbd.type(result)
		pyautogui.click((x + w / 2), (y + 100))
		self.solving_captcha = False

	def check_for_antibot(self):
		x = self.quest_window_x
		y = self.quest_window_y
		w = 310
		h = 400
		image = ImageGrab.grab(bbox=(x, y, w + x, h + y))
		text = pytesseract.image_to_string(image)
		if "captcha" in text:
			self.solving_captcha = True
			self.solve_captcha()
		else:
			pass

	def arrived_at_npc(self):
		x = self.quest_window_x
		y = self.quest_window_y
		w = 310 + x
		h = 20 + y
		image = ImageGrab.grab(bbox=(x, y, w, h))
		rgb = image.getpixel((200, 10))
		if rgb == (16, 25, 52):
			return True
		else:
			return False

	def get_screen_position(self, pos):
		return (pos[0] + self.offset_x, pos[1] + self.offset_y)

	def start(self):
		self.stopped = False
		t = Thread(target=self.run)
		t.start()

	def stop(self):
		self.stopped = True

	def run(self):
		while not self.stopped:
			start = time()
			if (time() - self.timestamp) > 30:
				self.check_for_antibot()
				self.timestamp = time()

			current_enemy_health = self.enemy_health()
			current_player_health = self.player_health()
			self.lock.acquire()
			self.current_enemy_health = current_enemy_health
			self.current_player_health = current_player_health
			self.lock.release()
			self.fps = round(1.0 / (time() - start), 1)