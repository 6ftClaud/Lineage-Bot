from pynput.mouse import Button, Controller
from threading import Thread, Lock
from time import sleep, time
from math import sqrt
import pyautogui
import keyboard
import os


from math import sqrt

class BotState:
	INITIALIZING = 0
	SEARCHING = 1
	ATTACKING = 2
	REBUFFING = 3

class BotActions:

	# settings
	INITIALIZING_SECONDS = 0

	# threading
	stopped = True
	lock = None

	# output
	message = ''

	# properties
	state = None
	targets = []
	offset_x = 0
	offset_y = 0
	window_w = 0
	window_h = 0
	player_health = 100
	enemy_health = 0
	buffed = True
	mouse = Controller()

	# abilitites (edit in main.py)
	DEBUFF = ''
	DAMAGE = ''
	SUSTAIN = ''
	TOGGLE = ''

	def __init__(self, offset_x, offset_y, w, h, INITIALIZING_SECONDS, abilities):
		self.lock = Lock()

		self.offset_x = offset_x
		self.offset_y = offset_y
		self.window_w = w
		self.window_h = h

		self.INITIALIZING_SECONDS = INITIALIZING_SECONDS
		self.state = BotState.INITIALIZING

		self.DEBUFF = abilities[0]
		self.DAMAGE = abilities[1]
		self.SUSTAIN = abilities[2]
		self.TOGGLE = abilities[-1]

	def target(self):
		target_i = 0
		targets = self.target_sorting(self.targets)

		while not self.stopped and target_i < len(targets):
			x, y = self.get_screen_position(targets[target_i])
			pyautogui.moveTo(x, y, _pause=False)
			keyboard.press('SHIFT')
			pyautogui.click()
			keyboard.release('SHIFT')
			if self.enemy_health > 99:
				self.message = f"Clicking at X: {x}, y: {y}"
				return True
			target_i += 1


	def attack(self):
		sleep(0.1)
		ability = self.DEBUFF
		keyboard.send(ability)
		while not self.stopped:
			if self.player_health < 70:
				ability = self.SUSTAIN
				keyboard.send(ability)
			else:
				ability = self.DAMAGE
				keyboard.send(ability)
			self.message = f"Clicking {ability}"
			sleep(0.05)
			if self.enemy_health == 0:
				keyboard.send('ESC')
				break

	def target_sorting(self, targets):
		my_pos = (self.window_w / 2, self.window_h / 2)
		def pythagorean_distance(pos):
			return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
		targets.sort(key=pythagorean_distance)
		# remove targets that are further away than SEARCH_RADIUS
		targets = [t for t in targets if pythagorean_distance(t) > 80]
		return targets

	def turn_camera(self, distance):
		pyautogui.moveTo((self.offset_x + self.window_w/2), (self.offset_y + self.window_h/2))
		self.mouse.press(Button.right)
		pyautogui.moveTo(distance, 0)
		self.mouse.release(Button.right)
		sleep(0.1)

	def get_screen_position(self, pos):
		return (pos[0] + self.offset_x, pos[1] + self.offset_y)

	def update_targets(self, targets):
		self.lock.acquire()
		self.targets = targets
		self.lock.release()

	def start(self):
		self.stopped = False
		t = Thread(target=self.run)
		t.start()

	def stop(self):
		self.stopped = True
		sleep(0.25)
		keyboard.send('F12')

		# this is the main logic controller
	def run(self):
		while not self.stopped:
			if self.state == BotState.INITIALIZING:
				sleep(self.INITIALIZING_SECONDS)
				sleep(0.25)
				keyboard.send('F12')
				self.lock.acquire()
				self.state = BotState.SEARCHING
				self.lock.release()

			elif self.state == BotState.SEARCHING:
				self.message = "Looking for enemies"
				if self.target():
					self.lock.acquire()
					self.state = BotState.ATTACKING
					self.lock.release()
				elif self.player_health <= 1:
					sleep(2)
					self.buffed = False
					self.lock.acquire()
					self.state = BotState.REBUFFING
					self.lock.release()
				else:
					self.turn_camera(250)

			elif self.state == BotState.ATTACKING:
				self.attack()
				self.lock.acquire()
				self.state = BotState.SEARCHING
				self.lock.release()

			elif self.state == BotState.REBUFFING:
				if self.buffed == False:
					pass
				else:
					self.lock.acquire()
					self.state = BotState.SEARCHING
					self.lock.release()

