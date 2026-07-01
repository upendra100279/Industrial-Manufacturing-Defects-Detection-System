"""
Schemas for inspection/detection responses.
"""
from pydantic import BaseModel
from datetime import datetime


class DetectionItem(BaseModel):
    class_name: str
    confidence: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    class Config:
        from_attributes = True


class InspectionResponse(BaseModel):
    id: int
    source_type: str
    original_filename: str | None
    processed_image_path: str | None
    is_defective: bool
    defect_count: int
    avg_confidence: float
    created_at: datetime
    detections: list[DetectionItem] = []

    class Config:
        from_attributes = True
