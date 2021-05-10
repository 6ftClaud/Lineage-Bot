import configparser
import argparse
import curses
import cv2 as cv
import keyboard
import os

from functions import *
from time import sleep
from time import time

# Check to see what Operating System is being used. Delete these 2 lines if you want to try anyway.
import platform
assert ('Linux' in platform.system()), "The bot only works on Linux."

# Set up config
path = os.path.dirname(os.path.abspath(__file__)) + '/settings.ini'
Config = configparser.ConfigParser()
Config.read(path)
UI_info = Config.get('Settings', 'UI_info')
titlebar = int(Config.get('Settings', 'Titlebar'))
border = int(Config.get('Settings', 'Border'))
to_village_offset = int(Config.get('Settings', 'To_village_offset'))
seconds = int(Config.get('Settings', 'Seconds'))
player_class = Config.get('Settings', 'Class')
abilities = Config.get('Settings', 'Abilities').split(",")

# Pass flags to DEBUG
DEBUG = None
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(add_help=False)
parser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS,
                    help='Debug flag is optional. Do not set anything to only see debug messages.')
parser.add_argument('--screen', dest='DEBUG', action='store_true',
                    help="Set to True if you want to see what the bot sees")
parser.add_argument('--no-screen', dest='DEBUG', action='store_false',
                    help="Set to False to only see ncurses output")
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
    bot = BotActions(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h,
                     seconds, abilities)
    bot.start()
    utils = Utils(wincap.offset_x, wincap.offset_y, wincap.w, wincap.h,
                  UI_info, wincap.screenshot, to_village_offset)
    utils.start()
    wincap.set_buff_bar_pos(utils.buff_bar_pos)
    if DEBUG is False:
        screen = curses.initscr()

    fps = 1
    while(True):

        start = time()
        vision.screenshot = wincap.screenshot
        utils.screenshot = wincap.screenshot

        if not utils.solving_captcha:
            if bot.state == BotState.INITIALIZING:
                os.system('xdotool windowactivate \
                $(xdotool search --onlyvisible --name "Lineage II")')
            elif bot.state == BotState.SEARCHING:
                bot.update_targets(vision.targets)
                bot.update_hp(utils.current_player_health, utils.current_enemy_health)
            elif bot.state == BotState.ATTACKING:
                bot.update_hp(utils.current_player_health, utils.current_enemy_health)
                bot.update_targets(vision.targets)
            elif bot.state == BotState.REBUFFING:
                if utils.rebuff():
                    bot.buffed = True
        elif utils.solving_captcha:
            bot.stop()
            if not utils.solving_captcha:
                bot.start()

        # shows bot vision
        if DEBUG is True:
            screenshot = wincap.screenshot
            for target in bot.targets:
                cv.circle(screenshot, (int(target[0]), int(
                    target[1])), 15, (0, 255, 0), 2)
            scale_percent = 60
            width = int(screenshot.shape[1] * scale_percent / 100)
            height = int(screenshot.shape[0] * scale_percent / 100)
            dim = (width, height)
            font = cv.FONT_HERSHEY_SIMPLEX
            resized = cv.resize(screenshot, dim, interpolation=cv.INTER_LINEAR)
            resized = cv.putText(resized, f"player health: {utils.current_player_health}%",
                                 (210, height - 85), font, 1, (0, 255, 0), 2, cv.LINE_AA)
            resized = cv.putText(resized, f"enemy health: {utils.current_enemy_health}%",
                                 (210, height - 55), font, 1, (0, 255, 0), 2, cv.LINE_AA)
            resized = cv.putText(resized, f"fps: {wincap.fps}",
                                 (210, height - 25), font, 1, (0, 255, 0), 2, cv.LINE_AA)
            cv.imshow('Matches', resized)
            cv.moveWindow('Matches', (wincap.offset_x + wincap.w), 0)
            cv.waitKey(1)
            if keyboard.is_pressed('q'):
                cv.destroyAllWindows()
                wincap.stop()
                vision.stop()
                bot.stop()
                utils.stop()
                break

        # output
        elif DEBUG is False:
            screen.clear()
            screen.addstr(f"Current player health is {utils.current_player_health}%\n")
            screen.addstr(f"Current enemy  health is {utils.current_enemy_health}%\n")
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

        elif DEBUG is None:
            if keyboard.is_pressed('q'):
                wincap.stop()
                vision.stop()
                bot.stop()
                utils.stop()
                break
        fps = round(1.0 / (time() - start), 1)


if __name__ == "__main__":
    main()
