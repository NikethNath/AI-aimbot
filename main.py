from screen_capture import capture_screen
from yolo_detector import detect_targets
from mouse_controller import move_mouse_in_two_strokes
import pyautogui
import keyboard
import cv2

aimbot_enabled = False
sensitivity_scale = 14  # 🔧 Adjust this to tune flick strength

def toggle_aimbot():
    global aimbot_enabled
    aimbot_enabled = not aimbot_enabled
    print(f"Aimbot {'enabled' if aimbot_enabled else 'disabled'}")

def draw_overlay(frame, boxes):
    for box in boxes:
        x1, y1, x2, y2, conf, cls = box
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    status = "Aimbot ON" if aimbot_enabled else "Aimbot OFF"
    cv2.putText(frame, status, (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255) if aimbot_enabled else (100, 100, 100), 2)

    return frame

def get_closest_target(boxes, center_x, center_y):
    def distance(box):
        x1, y1, x2, y2, *_ = box
        tx = (x1 + x2) / 2
        ty = (y1 + y2) / 2
        return (tx - center_x)**2 + (ty - center_y)**2
    return sorted(boxes, key=distance)[0]

def main():
    print("Press F8 to toggle aimbot. Press ESC to exit.")
    keyboard.add_hotkey('W', toggle_aimbot)  # Fixed to match F8 as mentioned
    cv2.namedWindow("Aimbot Overlay", cv2.WINDOW_NORMAL)

    screen_width, screen_height = pyautogui.size()
    center_x = screen_width // 2
    center_y = screen_height // 2

    global aimbot_enabled
    # i=0
    while True:
        frame = capture_screen()
        boxes = detect_targets(frame)

        # Continuous targeting - always aim at closest target when enabled
        if aimbot_enabled and boxes.shape[0] > 0:
            x1, y1, x2, y2, conf, cls = get_closest_target(boxes, center_x, center_y)
            target_x = int((x1 + x2) / 2)
            target_y = int((y1 + y2) / 2)

            dx = target_x - center_x
            dy = target_y - center_y
            # print(dx)
            # print(dy)

            move_mouse_in_two_strokes(dx, dy, sensitivity_scale)
            # i=i+1
           

        frame = draw_overlay(frame, boxes)
        cv2.imshow("Aimbot Overlay", frame)

        if cv2.waitKey(1) == 27:  # ESC key to exit
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()