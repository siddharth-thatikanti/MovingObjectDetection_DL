# Improved YOLOv9 for Moving Object Detection with Speed Estimation

## 1. Project Overview

This project implements an **Improved YOLOv9-based Moving Object Detection System** designed to:

* Detect moving objects (cars, pedestrians, cyclists)
* Improve detection for **fast-moving objects**
* Reduce bounding box flickering
* Estimate object **speed**
* Perform **real-time detection on video**
* Deploy via **API / Local System**

Dataset used: **KITTI Dataset**

---

## 2. Features

* YOLOv9 object detection
* Optical Flow motion enhancement
* Temporal frame processing
* DeepSORT / Kalman tracking
* Speed estimation
* FastAPI deployment
* Works on video, webcam, and images

---

## 3. Project Directory Structure

```
Improved-YOLOv9-Motion/
│
├── dataset/
│   ├── images/
│   │   ├── train/
│   │   └── val/
│   ├── labels/
│   │   ├── train/
│   │   └── val/
│   └── data.yaml
│
├── models/
│   ├── yolov9_base.yaml
│   └── yolov9_motion.yaml
│
├── src/
│   ├── optical_flow.py
│   ├── temporal_loader.py
│   ├── speed_estimator.py
│   ├── tracker.py
│   └── inference.py
│
├── runs/
│   └── (training outputs)
│
├── train.py
├── evaluate.py
├── deploy_api.py
├── requirements.txt
└── README.md
```

---

## 4. Miniconda Environment Setup

### Step 1 — Install Miniconda

Download: https://docs.conda.io/en/latest/miniconda.html

### Step 2 — Create Environment

Open **Anaconda Prompt** and run:

```bash
conda create -n yolov9_motion python=3.10 -y
conda activate yolov9_motion
```

---

## 5. Install Requirements

Create `requirements.txt`:

```
torch
torchvision
ultralytics
opencv-python
numpy
matplotlib
scipy
fastapi
uvicorn
filterpy
scikit-image
```

Install:

```bash
pip install -r requirements.txt
```

If GPU available:

```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu121
```

---

## 6. Dataset Setup

Dataset format (YOLO format):

```
class x_center y_center width height
```

Example label file:

```
0 0.52 0.48 0.30 0.25
```

### data.yaml

```yaml
path: dataset
train: images/train
val: images/val

names:
  0: car
  1: pedestrian
  2: cyclist
```

---

## 7. Training the Model

Run:

```bash
python train.py
```

OR

```bash
yolo task=detect model=models/yolov9_motion.yaml data=dataset/data.yaml epochs=120 imgsz=1280 batch=8 device=0
```

Training results saved in:

```
runs/detect/train/
```

Best model:

```
runs/detect/train/weights/best.pt
```

---

## 8. Run Inference (Detection on Video)

```bash
python src/inference.py
```

For webcam:

```python
cv2.VideoCapture(0)
```

For video file:

```python
cv2.VideoCapture("video.mp4")
```

---

## 9. Speed Estimation Logic

Speed formula:

```
speed = distance between object centers / time
```

Implemented in:

```
src/speed_estimator.py
```

---

## 10. Run Tracking + Speed Detection

```bash
python src/inference.py --track --speed
```

Output shows:

* Bounding boxes
* Object ID
* Object Speed

---

## 11. Run API Deployment

```bash
uvicorn deploy_api:app --host 0.0.0.0 --port 8000
```

Open:

```
http://127.0.0.1:8000/docs
```

Upload image → Get detections.

---

## 12. Export Model (Optional)

Export to ONNX:

```bash
yolo export model=runs/detect/train/weights/best.pt format=onnx
```

---

## 13. How to Run Project in Another Local PC (After Download ZIP)

### Step-by-Step

#### Step 1 — Install Miniconda

#### Step 2 — Extract ZIP

#### Step 3 — Open Anaconda Prompt

#### Step 4 — Go to Project Folder

```bash
cd path\to\Improved-YOLOv9-Motion
```

#### Step 5 — Create Environment

```bash
conda create -n yolov9_motion python=3.10 -y
conda activate yolov9_motion
```

#### Step 6 — Install Requirements

```bash
pip install -r requirements.txt
```

#### Step 7 — Run Inference (Using Trained Model)

```bash
python src/inference.py
```

#### Step 8 — If Training Needed

```bash
python train.py
```

#### Step 9 — Run API

```bash
uvicorn deploy_api:app --host 0.0.0.0 --port 8000
```

---

## 14. Important Notes

| Problem             | Solution             |
| ------------------- | -------------------- |
| Module not found    | Install requirements |
| GPU not detected    | Install CUDA torch   |
| Dataset error       | Check data.yaml      |
| Boxes flickering    | Enable tracking      |
| Fast objects missed | Use optical flow     |

---

## 15. Expected Output

The system will:

* Detect moving objects
* Track objects
* Estimate speed
* Work in real time
* Provide stable bounding boxes

---

## 16. Author

Improved YOLOv9 Moving Object Detection Project
Using Optical Flow + Tracking + Speed Estimation

---

## 17. Commands Summary (Quick Run)

```
conda create -n yolov9_motion python=3.10 -y
conda activate yolov9_motion
pip install -r requirements.txt
python train.py
python src/inference.py
uvicorn deploy_api:app --host 0.0.0.0 --port 8000
```

---
