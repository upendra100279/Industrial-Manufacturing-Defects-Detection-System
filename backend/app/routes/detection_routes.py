"""
Image upload + defect detection endpoints.
"""
import os
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.middleware.jwt_middleware import get_current_user
from app.models.user import User
from app.models.inspection import Inspection
from app.schemas.inspection_schema import InspectionResponse
from app.services.detection_service import process_image_detection

router = APIRouter()

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png", "image/jpg"}


@router.post("/image", response_model=InspectionResponse)
async def detect_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type: {file.content_type}. Use JPEG or PNG.",
        )

    inspection = await process_image_detection(db, file, current_user.id)
    return inspection


@router.get("/result/{inspection_id}/image", response_class=FileResponse)
def download_processed_image(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    inspection = (
        db.query(Inspection)
        .filter(Inspection.id == inspection_id, Inspection.user_id == current_user.id)
        .first()
    )
    if not inspection or not inspection.processed_image_path:
        raise HTTPException(status_code=404, detail="Processed image not found")

    if not os.path.exists(inspection.processed_image_path):
        raise HTTPException(status_code=404, detail="Image file missing on disk")

    return FileResponse(inspection.processed_image_path, media_type="image/jpeg")
