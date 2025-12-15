
import mss
import numpy as np
import cv2

# Initialize once at module level
sct = mss.mss()
monitor = sct.monitors[1]
buffer = np.zeros((monitor["height"], monitor["width"], 4), dtype=np.uint8)

def capture_screen():
    """Fast screen capture using pre-allocated buffer"""
    img = sct.grab(monitor)
    np.copyto(buffer, np.asarray(img))
    return cv2.cvtColor(buffer, cv2.COLOR_BGRA2BGR)

def close_capturer():
    """Clean up when done"""
    sct.close()
