from bot import BotActions, BotState
from capture import WindowCapture
from vision import Vision
from utils import Utils
import cv2 as cv
import numpy as np
import os
import keyboard
import curses
import argparse
from time import time, sleep

# Global Settings
# full Lineage II /system/WindowsInfo.ini path
UI_info = "/home/claud/.wine/drive_c/Program Files/Lineage II/system/WindowsInfo.ini"
# titlebar and border size in px
titlebar = 26
border = 2
# how long to wait until the bot starts
seconds = 4
# Set Archer/Mage
player_class = "Mage"

# abilities - DEBUFF, DAMAGE, SUSTAIN, NOBLESSE, TOGGLE 
abilities = ['F1', 'F2', 'F3', 'F12']
DEBUG = None
parser = argparse.ArgumentParser()
parser.add_argument('--debug', dest='DEBUG', action='store_true', help="Set to True if you want to see what the bot sees")
parser.add_argument('--no-debug', dest='DEBUG', action='store_false', help="Set to False to only see console output")
parser.set_defaults(DEBUG=False)
args = parser.parse_args()
DEBUG = args.DEBUG

wincap = WindowCapture(border, titlebar)
wincap.start()
while wincap.screenshot is None:
	sleep(0.01)
vision = Vision(wincap.screenshot)
vision.start()
bot = BotActions(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h, seconds, abilities)
bot.start()
utils = Utils(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h, UI_info, wincap.screenshot)
utils.start()
wincap.set_buff_bar_pos(utils.buff_bar_pos)

if DEBUG == False:
	screen = curses.initscr()

fps = 0
while(True):

	start = time()
	vision.update_screenshot(wincap.screenshot)
	utils.update_screenshot(wincap.screenshot)
	
	if not utils.solving_captcha:
		if bot.state == BotState.INITIALIZING:
			os.system('xdotool windowactivate $(xdotool search --onlyvisible --name "Lineage II")')
		elif bot.state == BotState.SEARCHING:
			bot.update_targets(vision.targets)
			bot.enemy_health = utils.current_enemy_health
			bot.player_health = utils.current_player_health
		elif bot.state == BotState.ATTACKING:
			bot.enemy_health = utils.current_enemy_health
			bot.player_health = utils.current_player_health
			bot.update_targets(vision.targets)
		elif bot.state == BotState.REBUFFING:
			if utils.rebuff():
				bot.player_health = utils.current_player_health
				bot.buffed = True

	elif utils.solving_captcha:
		bot.stop()
		while True:
			if not utils.solving_captcha:
				bot.start()
				break

	
	# slow, use only for debugging
	if DEBUG == True:
		screenshot = wincap.screenshot
		for target in bot.targets:
			cv.circle(screenshot, (int(target[0]), int(target[1])), 15, (0, 255, 0), 2)
		scale_percent = 60
		width = int(screenshot.shape[1] * scale_percent / 100)
		height = int(screenshot.shape[0] * scale_percent / 100)
		dim = (width, height)
		font = cv.FONT_HERSHEY_SIMPLEX
		resized = cv.resize(screenshot, dim, interpolation = cv.INTER_AREA)
		resized = cv.putText(resized, f"player health: {utils.current_player_health}%",(210, height - 85), font, 1, (0, 255, 0), 2, cv.LINE_AA)
		resized = cv.putText(resized, f"enemy health: {utils.current_enemy_health}%",(210, height - 55), font, 1, (0, 255, 0), 2, cv.LINE_AA)
		resized = cv.putText(resized, f"fps: {wincap.fps}",(210, height - 25), font, 1, (0, 255, 0), 2, cv.LINE_AA)
		cv.imshow('Matches', resized)
		cv.moveWindow('Matches', (wincap.offset_x + wincap.w), 0)
		key = cv.waitKey(1)
		if keyboard.is_pressed('q'):
			cv.destroyAllWindows()
			wincap.stop()
			vision.stop()
			bot.stop()
			utils.stop()
			break

	elif DEBUG == False:
		# output
		screen.clear()
		screen.addstr(f"Current player health is {utils.current_player_health}%\n")
		screen.addstr(f"Current enemy health is {utils.current_enemy_health}%\n")
		screen.addstr(f"{bot.message}\n\n")
		screen.addstr(f"Main loop fps: {fps}\n")
		screen.addstr(f"capture fps: {wincap.fps}\n")
		screen.addstr(f"bot fps: {bot.fps}\n")
		screen.addstr(f"utils fps: {utils.fps}\n")
		screen.addstr(f"vision fps: {vision.fps}\n")
		screen.refresh()
		if keyboard.is_pressed('q'):
			wincap.stop()
			vision.stop()
			bot.stop()
			utils.stop()
			curses.endwin()
			break
	fps = round(1.0 / (time() - start), 1)
	

exit(1)
