import requests
import cv2 as cv
import pytesseract
import os
from PIL import Image
pytesseract.pytesseract.tesseract_cmd = r'/usr/bin/tesseract'
os.environ['TESSDATA_PREFIX'] = '/usr/share/tessdata'

api_key = 'd6aaaaa8d888957'
payload = {'isOverlayRequired': False,
               'apikey': api_key,
               'OCREngine': 2,
               'language': 'eng',
               }

image = cv.imread('captcha.png')
image = cv.cvtColor(image, cv.COLOR_RGB2GRAY)
image = cv.threshold(image, 0, 255, cv.THRESH_BINARY| cv.THRESH_OTSU)[1]
image = cv.medianBlur(image, 1)
cv.imwrite('captcha2.png', image)
text = pytesseract.image_to_string('captcha.png')
print(text)

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

