from bot import BotActions, BotState
from capture import WindowCapture
from vision import Vision
from time import time, sleep
from utils import Utils
import cv2 as cv
import numpy as np
import os
import keyboard
import curses


import configparser
Config = configparser.ConfigParser()
Config.read("settings.ini")
UI_info = Config.get('Settings', 'UI_info')
titlebar = int(Config.get('Settings', 'Titlebar'))
border = int(Config.get('Settings', 'Border'))
to_village_offset = int(Config.get('Settings', 'To_village_offset'))
seconds = int(Config.get('Settings', 'Seconds'))
player_class = Config.get('Settings', 'Class')
abilities = Config.get('Settings', 'Abilities').split(",")


import argparse
DEBUG = None
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, help='Debug flag is optional. Do not set anything to only see debug messages.')
parser.add_argument('--screen', dest='DEBUG', action='store_true', help="Set to True if you want to see what the bot sees")
parser.add_argument('--no-screen', dest='DEBUG', action='store_false', help="Set to False to only see ncurses output")
parser.set_defaults(DEBUG=None)
args = parser.parse_args()
DEBUG = args.DEBUG


def main():

	wincap = WindowCapture(border, titlebar)
	wincap.start()
	while wincap.screenshot is None:
		sleep(0.01)
	vision = Vision(wincap.screenshot)
	vision.start()
	bot = BotActions(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h, seconds, abilities)
	bot.start()
	utils = Utils(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h, UI_info, wincap.screenshot, to_village_offset)
	utils.start()
	wincap.set_buff_bar_pos(utils.buff_bar_pos)
	
	if DEBUG == False:
		screen = curses.initscr()

	fps = 1
	while(True):

		start = time()
		vision.screenshot = wincap.screenshot
		utils.screenshot = wincap.screenshot
		bot.update_targets(vision.targets)
		bot.update_hp(utils.current_player_health, utils.current_enemy_health)
		bot.sleep_between_targeting = (1 / wincap.fps + 1 / utils.fps + 1 / fps + 0.15) # + lag
		bot.sleep_between_turning = (1 / vision.fps + 0.15)
		
		if not utils.solving_captcha:
			if bot.state == BotState.INITIALIZING:
				os.system('xdotool windowactivate $(xdotool search --onlyvisible --name "Lineage II")')
			elif bot.state == BotState.SEARCHING:
				pass
			elif bot.state == BotState.ATTACKING:
				pass
			elif bot.state == BotState.REBUFFING:
				if utils.rebuff():
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
			resized = cv.resize(screenshot, dim, interpolation = cv.INTER_LINEAR)
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
			screen.addstr(f"Current player health is {bot.player_health}%\n")
			screen.addstr(f"Current enemy  health is {bot.enemy_health}%\n")
			screen.addstr(f"{bot.message}\n\n")
			screen.addstr(f"main    fps: {fps}\n")
			screen.addstr(f"capture fps: {wincap.fps}\n")
			screen.addstr(f"utils   fps: {utils.fps}\n")
			screen.addstr(f"vision  fps: {vision.fps}\n")
			screen.refresh()
			if keyboard.is_pressed('q'):
				wincap.stop()
				vision.stop()
				bot.stop()
				utils.stop()
				curses.endwin()
				break

		elif DEBUG == None:
			if keyboard.is_pressed('q'):
				wincap.stop()
				vision.stop()
				bot.stop()
				utils.stop()
				break
		fps = round(1.0 / (time() - start), 1)

if __name__=="__main__":
    main()