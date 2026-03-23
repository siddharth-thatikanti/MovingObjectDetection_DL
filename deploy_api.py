from fastapi import FastAPI, UploadFile
import cv2
from ultralytics import YOLO

app = FastAPI()
model = YOLO("best.pt")

@app.post("/detect")
async def detect(file: UploadFile):
    image = cv2.imdecode(
        np.frombuffer(await file.read(), np.uint8),
        cv2.IMREAD_COLOR
    )
    results = model(image)
    return {"detections": results[0].boxes.data.tolist()}
