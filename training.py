from ultralytics import YOLO
model = YOLO('C:/Users/niket/Desktop/aimbot/yolov5s.pt')
model.train(data='C:/Users/niket/Desktop/kovaaks_dataset/data.yaml', epochs=50, imgsz=640, batch=16, name='kovaaks_aimbot')
