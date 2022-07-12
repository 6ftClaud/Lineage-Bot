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
As admin (`sudo su`)  
```  
git clone https://github.com/6ftClaud/Lineage-Bot  
pacman -S (or apt install) wmctrl xdotool  
pip install -r requirements.txt  
```  
edit settings.ini in project directory  
### Usage  
As admin (`sudo su`) in project directory  
```  
python main.py
```  
Available flags:  
--screen : run it with a screen that shows what the bot sees:  
--no-screen : run it with an ncurses console window  
none : runs without any output whatsoever  
e.g. `python main.py --screen`  
  
Press 'q' any time to stop the bot.  
