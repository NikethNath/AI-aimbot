import win32api
import win32con
import time

def move_mouse(dx, dy, sensitivity_scale=1.0):
    if(abs(dy)>200):
        if(dy<200):
            dy=dy-((0.2*dy)+31)
        else:
            dy=dy-((0.2*dy)-31)

    if(abs(dx)>350):
        if(dx<350):
            dx=dx-((0.4*dx)+130)
        else:
            dx=dx-((0.4*dx)-130)



    total_dx = dx * sensitivity_scale
    total_dy = dy * sensitivity_scale


    flick1_dx = int(total_dx)
    flick1_dy = int(total_dy)
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, flick1_dx, flick1_dy, 0, 0)
    time.sleep(0.007)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0,0,0)
    time.sleep(0.007)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0,0,0)
