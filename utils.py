from PIL import Image, ImageGrab
from threading import Thread, Lock
import keyboard
from pynput import keyboard
import pyautogui
import cv2 as cv
from time import sleep


class Utils:

	# settings
	MATCH_THRESHOLD = 0.85
	DEBUG = False
	# output
	player_health = 100
	enemy_health = 0
	# properties
	screenshot = None
	max_player_health = 150.0
	max_enemy_health = 150.0
	current_player_health = 100
	current_enemy_health = 100

	player_hp_x_pos = 0
	player_hp_y_pos = 0
	player_hp_bar_width = 0
	player_hp_bar_height = 0

	enemy_hp_x_pos = 0
	enemy_hp_y_pos = 0
	enemy_hp_bar_width = 0
	enemy_hp_bar_height = 0

	buff_bar_pos = (0, 0)

	def __init__(self, offset_x, offset_y, DEBUG, UI_info):
		self.lock = Lock()
		self.DEBUG = DEBUG

		self.tovillage = cv.imread('img/tovillage.png', cv.IMREAD_UNCHANGED)
		self.noblesse = cv.imread('img/noblesse.png', cv.IMREAD_UNCHANGED)
		self.farmingzones = cv.imread('img/farmingzones.png', cv.IMREAD_UNCHANGED)
		self.dmg1 = cv.imread('img/dmg1.png', cv.IMREAD_UNCHANGED)

		self.get_UI_positions(UI_info, offset_x, offset_y)

	def get_UI_positions(self, UI_info, offset_x, offset_y):
		lines = []
		with open(UI_info, 'r') as file:
			for line in file:
				if "=" in line:
					variable, value = line.split('=')
					lines.append(value)

		player_status = lines[16:18]
		self.player_hp_x_pos = int(float(player_status[0])) + offset_x + 16
		self.player_hp_y_pos = int(float(player_status[1])) + offset_y + 41
		self.player_hp_bar_width = 150
		self.player_hp_bar_height = 1

		enemy_status = lines[24:26]
		self.enemy_hp_x_pos = int(float(enemy_status[0])) + offset_x + 16
		self.enemy_hp_y_pos = int(float(enemy_status[1])) + offset_y + 26
		self.enemy_hp_bar_width = 150
		self.enemy_hp_bar_height = 1

		self.buff_bar_pos = (lines[40], lines[41])



	def player_health(self):
		current_player_health = 0.0
		im = ImageGrab.grab(bbox=(self.player_hp_x_pos, self.player_hp_y_pos, self.player_hp_bar_width + self.player_hp_x_pos, self.player_hp_bar_height + self.player_hp_y_pos))
		width, height = im.size
		for x in range(width):
			for y in range(height):
				rgb = im.getpixel((x, y))
				if rgb[0] >= 214:
					current_player_health += 1.0
		percent_health = current_player_health * 100.0 / self.max_player_health
		percent_health = round(percent_health, 1)
		if self.DEBUG == True:
			im.save(f'/home/claud/Code/LineageBot/debugimg/player_health.png')
		return percent_health

	def enemy_health(self):
		current_enemy_health = 0
		im = ImageGrab.grab(bbox=(self.enemy_hp_x_pos, self.enemy_hp_y_pos, self.enemy_hp_bar_width + self.enemy_hp_x_pos, self.enemy_hp_bar_height + self.enemy_hp_y_pos))
		width, height = im.size
		for x in range(width):
			for y in range(height):
				rgb = im.getpixel((x, y))
				if rgb[0] == 214:
					current_enemy_health += 1.0
		enemy_percent_health = current_enemy_health * 100.0 / self.max_enemy_health
		enemy_percent_health = round(enemy_percent_health, 1)
		if self.DEBUG == True:
			im.save(f'/home/claud/Code/LineageBot/debugimg/enemy_health.png')
		return enemy_percent_health

		# VEEEERY sketchy but that's the only way it works
	def target(self, text):
		keyboard = keyboard.Controller()
		try:
			keyboard.send('ENTER')
			keyboard.type(text)
			keyboard.send('ENTER')
		except:
			raise Exception("Could not target successfully")

	def click_image_on_screen(self, image):
		sleep(1.5)
		result = None
		try:
			while not result:
				result = cv.matchTemplate(self.screenshot, image, cv.TM_CCOEFF_NORMED)
				min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
				if max_val >= self.MATCH_THRESHOLD:
					max_loc = self.get_screen_position(max_loc)
					pyautogui.click(max_loc[0], max_loc[1])
		except:
			raise Exception("Could not find image on screen")

	def rebuff(self):
		self.message = f"Rebuffing"
		try:
			sleep(3)
			self.click_image_on_screen(self.tovillage)
			sleep(5)
			keyboard.send('F11')
			self.target("/target gatekeeper")
			self.target("/target gatekeeper")
			sleep(15)
			self.click_image_on_screen(self.farmingzones)
			self.click_image_on_screen(self.dmg1)
			return True
		except:
			raise Exception ("Could not rebuff.")

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
			current_player_health = self.player_health()
			current_enemy_health = self.enemy_health()
			self.lock.acquire()
			self.current_player_health = current_player_health
			self.current_enemy_health = current_enemy_health
			self.lock.release()