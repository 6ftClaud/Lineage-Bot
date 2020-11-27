import requests
import cv2 as cv
import pytesseract
import os
from PIL import Image, ImageGrab
import numpy as np
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/usr/share/tessdata'
data = os.popen('wmctrl -lG | grep "Lineage II"').read()
variables = data.split()
offset_x = int(float(variables[2]))
offset_y = int(float(variables[3]))
window_w = int(float(variables[4]))
window_h = int(float(variables[5]))

x = 0 + 50 + offset_x
y = 199 + 115 + offset_y
w = 190
h = 50
print(x, y, w, h)
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
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
f_path = BASE_DIR + "/img/captcha.png"
cv.imwrite(f_path, image)

with open(f_path, 'rb') as f:
	j = requests.post('https://api.ocr.space/parse/image', files={f_path: f}, data=payload).json()
	if j['ParsedResults']:
		result = j['ParsedResults'][0]['ParsedText']

"""
f_path = "captcha.png"
with open(f_path, 'rb') as f:
    j = requests.post('https://api.ocr.space/parse/image', files={f_path: f}, data=payload).json()
    if j['ParsedResults']:
        result = j['ParsedResults'][0]['ParsedText']
        print(result)

# d6aaaaa8d888957
# 84 184 308 75
"""

