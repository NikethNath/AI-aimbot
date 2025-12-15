from screen_capture import capture_screen
from yolo_detector import detect_targets
from mouse_controller import move_mouse
import pyautogui
import keyboard
import cv2
import numpy as np

aimbot_enabled = False
sensitivity_scale = 14
SHOW_OVERLAY = False  # 🔧 Toggle this to enable/disable overlay

def toggle_aimbot():
    global aimbot_enabled
    aimbot_enabled = not aimbot_enabled
    print(f"Aimbot {'enabled' if aimbot_enabled else 'disabled'}")

def get_closest_target(boxes, center_x, center_y):
    if boxes.shape[0] == 0:  # No targets detected
        return None
    
    def distance(box):
        x1, y1, x2, y2, *_ = box
        tx = (x1 + x2) / 2
        ty = (y1 + y2) / 2
        return (tx - center_x)**2 + (ty - center_y)**2
    
    # Return the closest target
    return min(boxes, key=distance)

def main():
    print("Press W to toggle aimbot. Press ESC to exit.")
    print("Overlay: DISABLED" if not SHOW_OVERLAY else "Overlay: ENABLED")
    keyboard.add_hotkey('W', toggle_aimbot)
    
    if SHOW_OVERLAY:
        cv2.namedWindow("Aimbot Overlay", cv2.WINDOW_NORMAL)

    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    frame_count = 0
    start_time = cv2.getTickCount()
    
    try:
        while True:
            # Capture screen
            frame_bgra = capture_screen()
            
            # Prepare for YOLO (fast slice)
            frame_for_yolo = frame_bgra[:, :, :3]
            boxes = detect_targets(frame_for_yolo)

            # Targeting logic - FIXED: Proper None check
            if aimbot_enabled and boxes.shape[0] > 0:
                target = get_closest_target(boxes, center_x, center_y)
                if target is not None:  # ✅ Proper None check
                    x1, y1, x2, y2, conf, cls = target
                    target_x = int((x1 + x2) / 2)
                    target_y = int((y1 + y2) / 2)
                    dx = target_x - center_x
                    dy = target_y - center_y
                    move_mouse(dx, dy, sensitivity_scale)

            # 🚀 PERFORMANCE CRITICAL: Skip overlay when disabled
            if SHOW_OVERLAY:
                # Convert and draw overlay
                frame_bgr = cv2.cvtColor(frame_bgra, cv2.COLOR_BGRA2BGR)
                for box in boxes:
                    x1, y1, x2, y2, conf, cls = box
                    x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
                    cv2.rectangle(frame_bgr, (x1, y1), (x2, y2), (0, 255, 0), 2)
                
                status = "Aimbot ON" if aimbot_enabled else "Aimbot OFF"
                cv2.putText(frame_bgr, status, (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if aimbot_enabled else (100, 100, 100), 2)
                cv2.imshow("Aimbot Overlay", frame_bgr)
                
                if cv2.waitKey(1) == 27:  # ESC key
                    break
            else:
                # 🚀 FAST PATH: Minimal operations
                # Still need to check for ESC even without overlay
                if cv2.waitKey(1) == 27:
                    break

            frame_count += 1
            
            # FPS counter
            if frame_count % 60 == 0:
                fps = 60 / ((cv2.getTickCount() - start_time) / cv2.getTickFrequency())
                print(f"FPS: {fps:.1f} | Targets: {boxes.shape[0]} | Aimbot: {'ON' if aimbot_enabled else 'OFF'}")
                start_time = cv2.getTickCount()
                
    except KeyboardInterrupt:
        pass
    finally:
        if SHOW_OVERLAY:
            cv2.destroyAllWindows()
        print("Aimbot stopped.")

if __name__ == "__main__":
    main()