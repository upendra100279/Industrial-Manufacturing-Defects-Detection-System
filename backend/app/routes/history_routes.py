"""
Inspection history endpoints.
"""
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import desc

from app.db.base import get_db
from app.middleware.jwt_middleware import get_current_user
from app.models.user import User
from app.models.inspection import Inspection
from app.schemas.inspection_schema import InspectionResponse

router = APIRouter()


@router.get("/", response_model=list[InspectionResponse])
def get_history(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    defective_only: bool = Query(False),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    query = (
        db.query(Inspection)
        .options(joinedload(Inspection.detections))
        .filter(Inspection.user_id == current_user.id)
    )

    if defective_only:
        query = query.filter(Inspection.is_defective == True)

    inspections = (
        query.order_by(desc(Inspection.created_at))
        .offset(skip)
        .limit(limit)
        .all()
    )
    return inspections


@router.get("/{inspection_id}", response_model=InspectionResponse)
def get_inspection_detail(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    inspection = (
        db.query(Inspection)
        .options(joinedload(Inspection.detections))
        .filter(Inspection.id == inspection_id, Inspection.user_id == current_user.id)
        .first()
    )
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")
    return inspection


@router.delete("/{inspection_id}", status_code=204)
def delete_inspection(
    inspection_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    inspection = (
        db.query(Inspection)
        .filter(Inspection.id == inspection_id, Inspection.user_id == current_user.id)
        .first()
    )
    if not inspection:
        raise HTTPException(status_code=404, detail="Inspection not found")

    db.delete(inspection)
    db.commit()
