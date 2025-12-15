import pyautogui
import time
import os

save_dir = r"C:\Users\niket\Desktop\kovaaks_dataset\images\train"
os.makedirs(save_dir, exist_ok=True)

for i in range(41,80):
    img = pyautogui.screenshot()
    img.save(os.path.join(save_dir, f"kovaak_{i:02d}.png"))
    time.sleep(2)  # Adjust delay as needed