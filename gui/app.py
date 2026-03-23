import os
import sys
from flask import Flask, render_template, request, send_file, Response

# --------------------------------------------------
# PROJECT ROOT
# --------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

# --------------------------------------------------
# IMPORT DETECTOR
# --------------------------------------------------
from gui.detector import process_image, process_video, webcam_frames

# --------------------------------------------------
# FLASK CONFIG
# --------------------------------------------------
app = Flask(
    __name__,
    template_folder=os.path.join(BASE_DIR, "templates"),
    static_folder=os.path.join(BASE_DIR, "static")
)

UPLOAD_DIR = os.path.join(BASE_DIR, "static", "uploads")
OUTPUT_DIR = os.path.join(BASE_DIR, "static", "outputs")

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# --------------------------------------------------
# ROUTES
# --------------------------------------------------

# 1️⃣ Welcome / Loading Page
@app.route("/")
def loading():
    return render_template("loading.html")

# 2️⃣ Dashboard
@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# 3️⃣ Image / Video Processing
@app.route("/run", methods=["POST"])
def run():
    mode = request.form.get("mode")
    file = request.files.get("file")

    if not file or file.filename == "":
        return "❌ No file uploaded", 400

    # ---------- IMAGE ----------
    if mode == "image":
        in_path = os.path.join(UPLOAD_DIR, "input.jpg")
        out_path = os.path.join(OUTPUT_DIR, "output.jpg")

        file.save(in_path)

        ok = process_image(in_path, out_path)
        if not ok or not os.path.exists(out_path):
            return "❌ Image processing failed", 400

        return send_file(out_path, mimetype="image/jpeg")

    # ---------- VIDEO ----------
    elif mode == "video":
        in_path = os.path.join(UPLOAD_DIR, "input.mp4")
        out_path = os.path.join(OUTPUT_DIR, "output.mp4")

        file.save(in_path)

        ok = process_video(in_path, out_path)
        if not ok or not os.path.exists(out_path):
            return "❌ Video processing failed", 400

        # ✅ IMPORTANT:
        # Do NOT send_file → render HTML player
        return render_template(
            "result_video.html",
            video_url="/static/outputs/output.mp4"
        )

    return "❌ Invalid mode selected", 400

# 4️⃣ LIVE WEBCAM STREAM (REAL-TIME)
@app.route("/webcam")
def webcam():
    return Response(
        webcam_frames(),
        mimetype="multipart/x-mixed-replace; boundary=frame"
    )

# --------------------------------------------------
# MAIN
# --------------------------------------------------
if __name__ == "__main__":
    print("🚀 Enhanced YOLOv9 App Running")
    print("📂 Base directory:", BASE_DIR)
    app.run(host="127.0.0.1", port=5000, debug=True)
