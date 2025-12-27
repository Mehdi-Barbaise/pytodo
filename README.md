# pytodo
-- Author: G3ngh1s

Graphical To-Do list made with Python

I remember an old exercise I made when I started learning python, that proposed to develop a simple CLI to-do-list app (many thanks to the author, I can't remember who it is though).
Now that I gained experience, I wanted to build a more advanced GUI version.

Tested on Gnome, KDE, and Windows 11 environments.

Requirements: 
- Python3
- PyQt5
- Qt-material

Features:
Add a task, sorted by due date, details while double-clicking on a task, mark it as "completed" (it then appears stripped and goes down the list), remove tasks, save tasks.

In the future, I plan to: 
- Correct some bugs (with the "--------------- Completed ---------------" line, that makes app crash when we select it and try to do "Remove" or "Mark as Completed")
- add a button to modify an existing task's information.
- Add a calender to choose a date instead by simply clicking on it.
