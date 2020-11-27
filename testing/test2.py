import time

import cv2
import mss
import numpy
import os
import cv2 as cv

window_rect = [0, 0, 0, 0]

data = os.popen('wmctrl -lG | grep "Lineage II"').read()
variables = data.split()
window_rect[0] = int(float(variables[2]))
window_rect[1] = int(float(variables[3]))
window_rect[2] = int(float(variables[4]))
window_rect[3] = int(float(variables[5]))

offset_x = window_rect[0]
offset_y = window_rect[1]
border_pixels = 2
titlebar_pixels = 26
cropped_x = border_pixels + offset_x
cropped_y = titlebar_pixels + offset_y

w = window_rect[2]
h = window_rect[3]

mon = {'top' : offset_y, 'left' : offset_x, 'width' : w, 'height' : h}
print(mon)


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

y = player_hp_y_pos
h = player_hp_bar_height + y
x = player_hp_x_pos
w = player_hp_bar_width + x



with mss.mss() as sct:
	# Part of the screen to capture

	while "Screen capturing":
		last_time = time.time()

		# Get raw pixels from the screen, save it to a Numpy array
		img = numpy.array(sct.grab(mon))

		y = player_hp_y_pos
		h = player_hp_bar_height + y
		x = player_hp_x_pos
		w = player_hp_bar_width + x
		im = img[y:h, x:w]
		cv.imwrite('test3.png', im)
		rgb = im[0]
		max_player_health = 30
		current_player_health = 0
		for r in range(0, len(rgb), 5):
			r = rgb[r][2]
			if r >= 214:
				current_player_health += 1.0
		percent_health = current_player_health * 100.0 / max_player_health
		percent_health = round(percent_health, 1)
		print(percent_health)
		break

		# Display the picture
		cv2.imshow("OpenCV/Numpy normal", img)

		# Display the picture in grayscale
		# cv2.imshow('OpenCV/Numpy grayscale',
		#            cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY))


		# Press "q" to quit
		if cv2.waitKey(25) & 0xFF == ord("q"):
			cv2.destroyAllWindows()
			break