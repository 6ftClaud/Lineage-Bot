## Lineage II bot using OpenCV  
### Video:
[![Lineage II bot using OpenCV](https://i.imgur.com/6iqhHLB.png)](http://www.youtube.com/watch?v=1KS7z7Z_g8Y)  
### Table of contents  
* [General info](#general-info)  
* [Technologies](#technologies)  
* [Setup](#setup)  
* [Usage](#usage)
### General info  
This bot uses OpenCV to find white text (enemies), targets them and hits them until they're all out of HP, at which point it switches targets. It also solves the Anti-Bot captcha and returns to village in case of death.  
### Technologies  
The bot uses OpenCV and PyAutoGui as it's 'main' modules.  
### Setup  
#### pip installation:  
```  
$ sudo su  
$ pip install opencv-lineage  
$ pacman -S (or apt install) wmctrl xdotool  
```  
edit '/usr/lib/python3.8/site-packages/opencv_lineage/settings.ini' file. 
#### cloning installation:  
```  
$ git clone https://github.com/6ftClaud/Lineage-Bot  
$ pacman -S (or apt install) wmctrl xdotool  
$ pip install numpy opencv-python PILLOW keyboard pyautogui pynput mss pytesseract requests  
```  
edit settings.ini  
### Usage  
The bot must be run as administrator (sudo).  
Run it with a screen that shows what the bot sees:  
```  
$ pip: opencv-lineage --screen  
$ cloned: sudo python main.py --screen  
```  
Run it with an ncurses console window  
```  
$ pip: opencv-lineage --no-screen  
$ cloned: sudo python main.py --no-screen  
```  
Run it without any output whatsoever:  
```  
$ pip: opencv-lineage  
$ cloned: sudo python main.py  
```  
Press 'q' any time to stop the bot.
