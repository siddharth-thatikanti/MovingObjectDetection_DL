from ultralytics import YOLO

model = YOLO("yolov9c.pt")
model.train(
    data="data.yaml",
    epochs=2,
    imgsz=640,
    batch=4,
    device="cpu"
)
