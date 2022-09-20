# Game Time Tracker

A CLI application to track time you've spent in a game.

## Purpose

If you play games on **_platforms that do not track time_**, 
but you really want to **_know how much time you've spent in a game_**, this is the right app for you!

## User scenario
1. Write down game `name` and it's `process` in `config.yml` as shown in the prompt in that file
2. Double click `START_ME.bat`
3. Leave the application running (minimize the window)
4. Close the application window as needed. 

_NOTE: If you close the application before the game process was terminated, the time will not be recorded!_

## Alternative use
The application may be used to track other processes as well, like messaging apps or word processors. 
Should you use it for this purpose, you might want to adjust the title of the table in `config.yml`:
change `table_title` to anything you like. You may change `title=` as well in `START_ME.bat`. 

## Limitations
This CLI **_supports Windows only_**. Sorry, Mac and Linux users. You are free to start the code from `main.py` any way you like. However, best user experience is not guaranteed in this case.