import cv2
import numpy as np
import time
from ultralytics import YOLO

# --------------------------------------------------
# MODEL LOAD (DETECT EVERYTHING)
# --------------------------------------------------
model = YOLO("yolov8m.pt")  # COCO-trained, detects 80 classes

# --------------------------------------------------
# SAFE FRAME ENHANCEMENT
# --------------------------------------------------
def enhance_frame(frame):
    if frame is None or frame.size == 0:
        return frame

    kernel = np.array([
        [0, -1, 0],
        [-1, 5, -1],
        [0, -1, 0]
    ])
    return cv2.filter2D(frame, -1, kernel)

# --------------------------------------------------
# CONFUSION HANDLING (UNKNOWN OBJECT)
# --------------------------------------------------
CONFUSION_CLASSES = {"giraffe", "horse", "zebra", "cow", "sheep", "dog"}

def resolve_unknown_objects(results, names, conf_threshold=0.40):
    for box in results.boxes:
        cls_id = int(box.cls)
        conf = float(box.conf)
        label = names[cls_id]

        if label in CONFUSION_CLASSES and conf < conf_threshold:
            box.cls = -1  # mark as unknown

# --------------------------------------------------
# DRAW RESULTS (SUPPORT UNKNOWN)
# --------------------------------------------------
def draw_results(frame, results):
    frame = frame.copy()

    for box in results.boxes:
        x1, y1, x2, y2 = box.xyxy[0].cpu().numpy().astype(int)
        conf = float(box.conf)

        if int(box.cls) == -1:
            label = f"Unknown Object {conf:.2f}"
            color = (0, 0, 255)  # red
        else:
            cls_id = int(box.cls)
            label = f"{model.names[cls_id]} {conf:.2f}"
            color = (0, 255, 0)  # green

        cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
        cv2.putText(
            frame, label,
            (x1, max(y1 - 10, 10)),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            color,
            2
        )

    return frame

# --------------------------------------------------
# IMAGE PROCESSING
# --------------------------------------------------
def process_image(input_path, output_path):
    img = None
    for _ in range(3):  # retry for webcam capture delay
        img = cv2.imread(input_path)
        if img is not None:
            break
        time.sleep(0.1)

    if img is None:
        print("❌ Failed to read image")
        return False

    img = enhance_frame(img)

    results = model(img, conf=0.25, iou=0.50, verbose=False)
    resolve_unknown_objects(results[0], model.names)
    output = draw_results(img, results[0])

    cv2.imwrite(output_path, output)
    return True

# --------------------------------------------------
# VIDEO PROCESSING (BROWSER-SAFE H.264)
# --------------------------------------------------
def process_video(input_path, output_path):
    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print("❌ Cannot open input video")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0 or fps > 120:
        fps = 25  # safe default

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    if width == 0 or height == 0:
        print("❌ Invalid video dimensions")
        cap.release()
        return False

    # ✅ CRITICAL FIX: H.264 codec (browser compatible)
    fourcc = cv2.VideoWriter_fourcc(*"avc1")

    out = cv2.VideoWriter(
        output_path,
        fourcc,
        fps,
        (width, height)
    )

    if not out.isOpened():
        print("❌ VideoWriter failed")
        cap.release()
        return False

    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            break

        frame = enhance_frame(frame)
        results = model(frame, conf=0.25, iou=0.50, verbose=False)

        resolve_unknown_objects(results[0], model.names)
        output = draw_results(frame, results[0])

        out.write(output)
        frame_count += 1

    cap.release()
    out.release()

    print(f"✅ Video saved successfully. Frames written: {frame_count}")
    return frame_count > 0

# --------------------------------------------------
# LIVE WEBCAM STREAM (MJPEG)
# --------------------------------------------------
def webcam_frames():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret or frame is None:
            continue

        frame = enhance_frame(frame)
        results = model(frame, conf=0.25, iou=0.50, verbose=False)

        resolve_unknown_objects(results[0], model.names)
        output = draw_results(frame, results[0])

        _, buffer = cv2.imencode(".jpg", output)
        yield (
            b"--frame\r\n"
            b"Content-Type: image/jpeg\r\n\r\n"
            + buffer.tobytes()
            + b"\r\n"
        )
