"""
Singleton service wrapping the YOLOv8 model.
Loaded ONCE at app startup (see main.py lifespan) and reused across all
requests. Inference runs in a thread pool to avoid blocking the event loop.
"""
import asyncio
import cv2
import numpy as np
import torch
from ultralytics import YOLO

from app.core.config import settings
from app.core.logging_config import logger


class YOLOService:
    def __init__(self):
        self.model: YOLO | None = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_model(self) -> None:
        try:
            self.model = YOLO(settings.YOLO_WEIGHTS_PATH)
            self.model.to(self.device)
            logger.info(f"YOLO model loaded on device='{self.device}' from "
                        f"{settings.YOLO_WEIGHTS_PATH}")
        except Exception as e:
            logger.warning(f"Could not load custom weights ({e}). "
                            f"Falling back to yolov8n.pt — train a custom "
                            f"model with ai-engine/src/train.py for real defect classes.")
            self.model = YOLO("yolov8n.pt")
            self.model.to(self.device)

    def _run_inference_sync(self, image: np.ndarray) -> list[dict]:
        results = self.model.predict(
            source=image,
            conf=settings.CONFIDENCE_THRESHOLD,
            device=self.device,
            verbose=False,
        )

        detections = []
        result = results[0]
        names = result.names

        for box in result.boxes:
            x1, y1, x2, y2 = box.xyxy[0].tolist()
            conf = float(box.conf[0])
            cls_id = int(box.cls[0])

            detections.append({
                "class_name": names[cls_id],
                "confidence": round(conf, 4),
                "x_min": x1, "y_min": y1, "x_max": x2, "y_max": y2,
            })

        return detections

    async def predict(self, image: np.ndarray) -> list[dict]:
        if self.model is None:
            raise RuntimeError("YOLO model not loaded. Call load_model() at startup.")

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._run_inference_sync, image)

    @staticmethod
    def read_image_bytes(file_bytes: bytes) -> np.ndarray:
        np_arr = np.frombuffer(file_bytes, np.uint8)
        return cv2.imdecode(np_arr, cv2.IMREAD_COLOR)


yolo_service = YOLOService()
