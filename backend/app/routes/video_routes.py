"""
Endpoints for webcam live-frame detection and video file upload detection.
"""
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import Response
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.middleware.jwt_middleware import get_current_user
from app.models.user import User
from app.schemas.inspection_schema import InspectionResponse
from app.services.video_service import detect_single_frame, process_video_upload
from app.services.yolo_service import yolo_service

router = APIRouter()


@router.post("/webcam-frame")
async def detect_webcam_frame(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
):
    raw_bytes = await file.read()
    image = yolo_service.read_image_bytes(raw_bytes)
    if image is None:
        raise HTTPException(status_code=400, detail="Could not decode frame")

    result = await detect_single_frame(image)
    return Response(content=result["annotated_jpeg_bytes"], media_type="image/jpeg")


@router.post("/upload", response_model=InspectionResponse)
async def detect_video_upload(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if file.content_type not in {"video/mp4", "video/avi", "video/quicktime"}:
        raise HTTPException(status_code=400, detail="Unsupported video format")

    inspection = await process_video_upload(db, file, current_user.id)
    return inspection
