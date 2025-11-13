A aimbot that uses a yolov5 model for detecting targets in a single pass from frames
generated on the screen. and pipelines the cordinates of the target to mouse_controller.py
which using win32api as well as win32con to both simulate mouse movement as well as
mouse clicks.

At this stage, the aimbot is only optimised to work on a 106 OW fov, along with 25cm/360 sensitivity
at 6400 dpi (Kovaak's settings) on only tile frenzy scenario. 
