## Lineage II bot using OpenCV  
### Table of contents  
* [General info](#general-info)  
* [Technologies](#technologies)  
* [Setup](#setup)  
* [Usage](#usage)
### General info  
This bot uses OpenCV to find white text (enemies), targets them and hits them 'until they're all out of HP, at which point it switches targets. It also solves the Anti-Bot captcha and returns to village in case of death.  
### Technologies  
The bot uses OpenCV and PyAutoGui as it's 'main' modules.  
### Setup  
To run this bot you need to run it on Linux. Installation:  
```  
$ cd sudo su  
$ pip install opencv-lineage  
$ pacman (or apt install) wmctrl xdotool  
```  
### Usage  
Run it with a screen that shows what the bot sees:  
```  
$ opencv-lineage --screen  
```  
Run it with an ncurses console window  
```  
$ opencv-lineage --no-screen  
```  
Run it without any output whatsoever:  
```  
$ opencv-lineage  
```  
