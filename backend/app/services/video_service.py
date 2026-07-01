"""
Handles webcam single-frame detection (no DB write) and video file
upload detection (sampled frames, aggregated, single Inspection row).
"""
import cv2
import numpy as np
from sqlalchemy.orm import Session

from app.services.yolo_service import yolo_service
from app.utils.image_utils import draw_detections, save_image
from app.utils.file_utils import save_upload_file, build_processed_path
from app.models.inspection import Inspection
from app.models.detection import Detection
from app.core.logging_config import logger

FRAME_SAMPLE_INTERVAL = 10


async def detect_single_frame(image: np.ndarray) -> dict:
    detections = await yolo_service.predict(image)
    annotated = draw_detections(image, detections)

    success, buffer = cv2.imencode(".jpg", annotated)
    if not success:
        raise RuntimeError("Failed to encode annotated frame")

    return {
        "detections": detections,
        "annotated_jpeg_bytes": buffer.tobytes(),
        "is_defective": len(detections) > 0,
    }


async def process_video_upload(db: Session, file, user_id: int) -> Inspection:
    original_path = save_upload_file(file)
    cap = cv2.VideoCapture(original_path)

    if not cap.isOpened():
        raise RuntimeError(f"Could not open video file: {original_path}")

    frame_idx = 0
    all_detections: list[dict] = []
    best_frame = None
    best_frame_detections: list[dict] = []
    best_frame_score = -1.0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % FRAME_SAMPLE_INTERVAL == 0:
            dets = await yolo_service.predict(frame)
            all_detections.extend(dets)

            frame_score = sum(d["confidence"] for d in dets)
            if frame_score > best_frame_score:
                best_frame_score = frame_score
                best_frame = frame
                best_frame_detections = dets

        frame_idx += 1

    cap.release()

    if best_frame is None:
        best_frame = np.zeros((480, 640, 3), dtype=np.uint8)

    annotated = draw_detections(best_frame, best_frame_detections)
    processed_path = build_processed_path(original_path)
    save_image(annotated, processed_path)

    avg_conf = (
        sum(d["confidence"] for d in all_detections) / len(all_detections)
        if all_detections else 0.0
    )

    inspection = Inspection(
        user_id=user_id,
        source_type="video",
        original_filename=file.filename,
        processed_image_path=processed_path,
        is_defective=len(all_detections) > 0,
        defect_count=len(all_detections),
        avg_confidence=round(avg_conf, 4),
    )
    db.add(inspection)
    db.flush()

    for d in best_frame_detections:
        db.add(Detection(
            inspection_id=inspection.id,
            class_name=d["class_name"], confidence=d["confidence"],
            x_min=d["x_min"], y_min=d["y_min"], x_max=d["x_max"], y_max=d["y_max"],
        ))

    db.commit()
    db.refresh(inspection)

    logger.info(
        f"Video inspection #{inspection.id}: sampled {frame_idx // FRAME_SAMPLE_INTERVAL} "
        f"frames, {len(all_detections)} total detections"
    )
    return inspection
