import keyboard
import pyautogui

from threading import Lock
from threading import Thread
from pynput.mouse import Button
from pynput.mouse import Controller
from time import sleep
from time import time
from math import sqrt


class BotState:
    INITIALIZING = 0
    SEARCHING = 1
    ATTACKING = 2
    REBUFFING = 3

class BotActions:

    # settings
    init_seconds = 0

    # threading
    stopped = True
    lock = None

    # output
    message = None

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
    sleep_between_targeting = 0
    sleep_between_turning = 0
    mouse = Controller()
    time = 0

    # abilitites (edit in settings.ini)
    DEBUFF = None
    DAMAGE = None
    SUSTAIN = None
    TOGGLE = None

    def __init__(self, offset_x, offset_y, w, h, init_seconds, abilities):
        self.lock = Lock()

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.window_w = w
        self.window_h = h

        self.init_seconds = init_seconds
        self.state = BotState.INITIALIZING

        self.DEBUFF = abilities[0]
        self.DAMAGE = abilities[1]
        self.SUSTAIN = abilities[2]
        self.TOGGLE = abilities[-1]

    def target(self):
        target_i = 0
        targets = self.target_sorting(self.targets)
        keyboard.press('SHIFT')
        while not self.stopped and target_i < len(targets):
            x, y = self.get_screen_position(targets[target_i])
            pyautogui.click(x, y + 25, _pause=False)
            sleep(self.sleep_between_targeting)
            if self.enemy_health == 100:
                self.message = f"Clicking at X: {x}, y: {y}"
                keyboard.release('SHIFT')
                return True
            target_i += 1
        keyboard.release('SHIFT')

    def attack(self):
        timestamp = time()
        ability = self.DEBUFF
        keyboard.send(ability)
        while not self.stopped:
            if (time() - timestamp) > 15:
                keyboard.send('ESC')
                self.turn_camera(500)
                break
            elif self.enemy_health == 0:
                keyboard.send('ESC')
                break
            elif self.player_health <= 70 and self.enemy_health > 0:
                ability = self.SUSTAIN
                keyboard.send(ability)
            elif self.player_health > 70 and self.enemy_health > 0:
                ability = self.DAMAGE
                keyboard.send(ability)
            self.message = f"Clicking {ability}"
            sleep(0.05)

    def target_sorting(self, targets):
        my_pos = (self.window_w / 2, self.window_h / 2)

        def pythagorean_distance(pos):
            return sqrt((pos[0] - my_pos[0])**2 + (pos[1] - my_pos[1])**2)
        targets.sort(key=pythagorean_distance)
        # remove targets that are further away than SEARCH_RADIUS
        targets = [t for t in targets if pythagorean_distance(t) > 100]
        return targets

    def turn_camera(self, distance):
        x = (self.offset_x + self.window_w / 2)
        y = (self.offset_y + self.window_h / 2)
        pyautogui.moveTo(x, y)
        self.mouse.press(Button.right)
        pyautogui.moveTo(distance, 0)
        self.mouse.release(Button.right)
        sleep(self.sleep_between_turning)

    def get_screen_position(self, pos):
        return (pos[0] + self.offset_x, pos[1] + self.offset_y)

    def update_targets(self, targets):
        self.lock.acquire()
        self.targets = targets
        self.lock.release()

    def update_hp(self, player, enemy):
        self.lock.acquire()
        self.enemy_health = enemy
        self.player_health = player
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
                sleep(self.init_seconds)
                sleep(0.25)
                keyboard.send('F12')
                self.lock.acquire()
                self.state = BotState.SEARCHING
                self.lock.release()

            elif self.state == BotState.SEARCHING:
                self.message = "Looking for enemies"
                if self.player_health == 0:
                    self.buffed = False
                    self.lock.acquire()
                    self.state = BotState.REBUFFING
                    self.lock.release()
                elif self.target():
                    self.lock.acquire()
                    self.state = BotState.ATTACKING
                    self.lock.release()
                else:
                    self.turn_camera(250)

            elif self.state == BotState.ATTACKING:
                self.attack()
                self.lock.acquire()
                self.state = BotState.SEARCHING
                self.lock.release()

            elif self.state == BotState.REBUFFING:
                if self.buffed:
                    self.lock.acquire()
                    self.state = BotState.SEARCHING
                    self.lock.release()
                else:
                    pass
