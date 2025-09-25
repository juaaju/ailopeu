import cv2
import numpy as np
from ultralytics import YOLO

def visualize_radius(frame, results, H_REF=120):
    """
    Tambah visualisasi radius (dekat & jauh) di bawah kendaraan
    berdasarkan bounding box YOLO.
    """
    overlay = frame.copy()
    count_vehicle = 0

    for box in results.boxes:
        cls_id = int(box.cls[0])
        if cls_id not in [2, 3, 5, 7]:  # car, motor, bus, truck
            continue

        count_vehicle += 1
        x1, y1, x2, y2 = map(int, box.xyxy[0].cpu().numpy())
        w_box, h_box = x2 - x1, y2 - y1
        cx, cy = x1 + w_box // 2, y2  # titik bawah tengah mobil

        # --- Skala radius berdasar tinggi bbox
        scale = max(0.3, h_box / H_REF)

        # Radius dekat (hijau)
        axes_near = (int(120 * scale), int(50 * scale))
        cv2.ellipse(
            overlay,
            (cx, cy),
            axes_near,
            angle=0,
            startAngle=200,  # setengah bawah
            endAngle=-20,
            color=(0, 255, 0),
            thickness=8,
            lineType=cv2.LINE_AA,
        )

        # Radius jauh (merah, full lingkaran)
        axes_far = (int(200 * scale), int(90 * scale))
        cv2.ellipse(
            overlay,
            (cx, cy),
            axes_far,
            angle=0,
            startAngle=0,
            endAngle=360,
            color=(0, 0, 255),
            thickness=8,
            lineType=cv2.LINE_AA,
        )

        # Bounding box opsional
        cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)

    # Gabungkan overlay dengan frame
    frame = cv2.addWeighted(overlay, 0.4, frame, 0.6, 0)
    return frame, count_vehicle


if __name__ == "__main__":
    print("[INFO] Loading YOLO model...")
    model = YOLO("E:/projek/ailopeu/ailopeu/models/yolov8n.pt")

    cap = cv2.VideoCapture("input.mp4")
    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    out = cv2.VideoWriter("output_with_2radius.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    frame_idx = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_idx += 1

        results = model(frame, verbose=False)[0]
        frame, count = visualize_radius(frame, results)

        if frame_idx % 10 == 0:
            print(f"[INFO] Frame {frame_idx}: Detected {count} vehicle(s).")

        out.write(frame)

    cap.release()
    out.release()
    print("[INFO] Done.")
