from ultralytics import YOLO
import numpy as np

# Load your trained YOLO model
try:
    model = YOLO('C:/Users/niket/Desktop/aimbot/runs/detect/kovaaks_aimbot/weights/best.pt')
    print("✅ YOLO model loaded successfully")
except Exception as e:
    print("❌ Failed to load YOLO model:", e)
    model = None

def detect_targets(frame):

    if model is None:
        print("⚠️ Model not loaded. Skipping detection.")
        return np.array([])

    try:
        results = model.predict(source=frame, verbose=False)
    except Exception as e:
        print("❌ YOLO prediction error:", e)
        return np.array([])

    boxes = []
    for r in results:
        if not hasattr(r, 'boxes') or r.boxes is None:
            continue
        for box in r.boxes:
            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            conf = box.conf[0].cpu().item()
            cls = box.cls[0].cpu().item()
            boxes.append([x1, y1, x2, y2, conf, cls])

    return np.array(boxes)