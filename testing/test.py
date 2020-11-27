import os
import subprocess
from PIL import Image, ImageGrab
import numpy as np
import pyautogui
import cv2 as cv
# find window offset
data = os.popen('wmctrl -lG | grep "Lineage II"').read()
variables = data.split()
offset_x = int(float(variables[2]))
offset_y = int(float(variables[3]))
window_w = int(float(variables[4]))
window_h = int(float(variables[5]))
max_player_health = 30.0
lines = []
with open('/home/claud/.wine/drive_c/Program Files/Lineage II/system/WindowsInfo.ini', 'r') as file:
	for line in file:
		if "=" in line:
			variable, value = line.split('=')
			lines.append(value)

player_status = lines[16:18]
player_hp_x_pos = int(float(player_status[0])) + 16
player_hp_y_pos = int(float(player_status[1])) + 41
player_hp_bar_width = 150
player_hp_bar_height = 1

enemy_status = lines[24:26]
enemy_hp_x_pos = int(float(enemy_status[0])) + 16
enemy_hp_y_pos = int(float(enemy_status[1])) + 26
enemy_hp_bar_width = 150
enemy_hp_bar_height = 12

buff_bar_pos = (lines[40], lines[41])

quest_window_x = int(float(lines[28]))
quest_window_y = int(float(lines[29]))


y = player_hp_y_pos
h = player_hp_bar_height + y
x = player_hp_x_pos
w = player_hp_bar_width + x
# (y:h+y, x:w+x)
img = ImageGrab.grab(bbox=(offset_x, offset_y, window_w + offset_x, window_h+ offset_y))
img = np.array(img)
img[int(buff_bar_pos[1]):105 + int(buff_bar_pos[1]), int(buff_bar_pos[0]):325 + int(buff_bar_pos[0])] = (0, 0, 0)
im = img[y:h, x:w]
cv.imwrite('test2.png', im)
rgb = im[0][:][:][:]
percent_health = 0
current_player_health = 0
for r in range(0, len(rgb), 5):
	r = rgb[r][0]
	if r >= 214:
		current_player_health += 1.0
percent_health = current_player_health * 100.0 / max_player_health
percent_health = round(percent_health, 1)
print(percent_health, current_player_health, max_player_health)

"""
current_player_health = 0
im = ImageGrab.grab(bbox=(player_hp_x_pos, player_hp_y_pos, player_hp_bar_width + player_hp_x_pos, player_hp_bar_height + player_hp_y_pos))
width, height = im.size
for x in range(0, width, 5):
	for y in range(height):
		rgb = im.getpixel((x, y))
		if rgb[0] >= 214:
			current_player_health += 1.0
im.save('/home/claud/Code/LineageBot/testing/test2.png')
percent_health = current_player_health * 100.0 / max_player_health
percent_health = round(percent_health, 1)
"""