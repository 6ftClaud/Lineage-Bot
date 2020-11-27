import os
import subprocess
from PIL import Image, ImageGrab
import pyautogui
# find window offset
data = os.popen('wmctrl -lG | grep "Lineage II"').read()
variables = data.split()
offset_x = int(float(variables[2]))
offset_y = int(float(variables[3]))
window_w = int(float(variables[4]))
window_h = int(float(variables[5]))

posX=0
posY=198

x = 0 + offset_x
y = 198 + offset_y
w = 310 + x
h = 20 + y
image = ImageGrab.grab(bbox=(x, y, w, h))
image = image.save('test.png')
"""
# Test offset
print(f"X offset is {offset_x}, Y offset is {offset_y}")
x, y = pyautogui.position()
print(x - offset_x, y - offset_y)
color = pyautogui.pixel(x, y)
print(color)
x = 0 + offset_x + 16
y = 0 + offset_y + 41
w = 150
h = 1
current_enemy_health = 0
im = ImageGrab.grab(bbox=(x, y, w + x, h + y))
im.save(f'/home/claud/Code/LineageBot/test.png')
width, height = im.size
current_enemy_health = 0
for x in range(width):
	for y in range(height):
		rgb = im.getpixel((x, y))
		if rgb[0] == 214:
			current_enemy_health +=1

print(current_enemy_health)

"""