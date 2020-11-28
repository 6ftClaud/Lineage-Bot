import os
import requests
from PIL import ImageGrab
import numpy as np
import cv2 as cv
import pyautogui
from pynput import keyboard
kbd = keyboard.Controller()
api_key = 'd6aaaaa8d888957'
payload = {'isOverlayRequired': False,
				'apikey': api_key,
				'OCREngine': 2,
				'language': 'eng',}
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
f_path = BASE_DIR + "/img/captcha.png"
with open(f_path, 'rb') as f:
	j = requests.post('https://api.ocr.space/parse/image', files={f_path: f}, data=payload).json()
	if j['ParsedResults']:
		result = j['ParsedResults'][0]['ParsedText']

if '.' or ',' in result:
	result = result.replace('.','')
	result = result.replace(',','')
print(result)