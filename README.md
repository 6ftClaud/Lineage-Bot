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
$ sudo su  
$ pacman -S (or apt install) wmctrl xdotool  
$ pip install numpy opencv-python PILLOW keyboard pyautogui pynput mss pytesseract requests  
```  
edit settings.ini  
### Usage  
##### pip:
```  
$ sudo su  
$ opencv-lineage  
```  
##### cloned:
```  
$ sudo su  
$ python main.py
```  
Available flags:  
--screen : run it with a screen that shows what the bot sees:  
--no-screen : run it with an ncurses console window  
none : runs without any output whatsoever  
e.g. opencv-lineage --screen  
  
Press 'q' any time to stop the bot.  
### TODO:  
Add Windows support using Interception driver to make mouse clicks work  
Add more classes (i.e. archer, spoiler) support  
Clean up main.py because it is looking hella ugly at the moment
