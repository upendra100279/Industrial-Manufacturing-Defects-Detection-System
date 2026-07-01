"""
Orchestrates a single detection request: decode, infer, draw, persist.
"""
from sqlalchemy.orm import Session

from app.services.yolo_service import yolo_service
from app.utils.image_utils import draw_detections, save_image
from app.utils.file_utils import save_upload_file, build_processed_path
from app.models.inspection import Inspection
from app.models.detection import Detection
from fastapi import UploadFile
from app.core.logging_config import logger


async def process_image_detection(
    db: Session, file: UploadFile, user_id: int
) -> Inspection:
    original_path = save_upload_file(file)

    with open(original_path, "rb") as f:
        image = yolo_service.read_image_bytes(f.read())

    detections = await yolo_service.predict(image)

    annotated = draw_detections(image, detections)
    processed_path = build_processed_path(original_path)
    save_image(annotated, processed_path)

    avg_conf = (
        sum(d["confidence"] for d in detections) / len(detections)
        if detections else 0.0
    )

    inspection = Inspection(
        user_id=user_id,
        source_type="image",
        original_filename=file.filename,
        processed_image_path=processed_path,
        is_defective=len(detections) > 0,
        defect_count=len(detections),
        avg_confidence=round(avg_conf, 4),
    )
    db.add(inspection)
    db.flush()

    for d in detections:
        db.add(Detection(
            inspection_id=inspection.id,
            class_name=d["class_name"],
            confidence=d["confidence"],
            x_min=d["x_min"], y_min=d["y_min"],
            x_max=d["x_max"], y_max=d["y_max"],
        ))

    db.commit()
    db.refresh(inspection)

    logger.info(
        f"Inspection #{inspection.id} by user {user_id}: "
        f"{len(detections)} defect(s) found"
    )
    return inspection
