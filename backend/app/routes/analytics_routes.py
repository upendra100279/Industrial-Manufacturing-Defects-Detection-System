"""
Dashboard and analytics endpoints.
"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.middleware.jwt_middleware import get_current_user
from app.models.user import User
from app.schemas.analytics_schema import DashboardStats, DefectFrequencyItem, TrendPoint
from app.services.analytics_service import get_dashboard_stats, get_defect_frequency, get_trend

router = APIRouter()


@router.get("/dashboard", response_model=DashboardStats)
def dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_dashboard_stats(db, current_user.id)


@router.get("/defect-frequency", response_model=list[DefectFrequencyItem])
def defect_frequency(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_defect_frequency(db, current_user.id)


@router.get("/trend", response_model=list[TrendPoint])
def trend(
    days: int = Query(14, ge=1, le=90),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return get_trend(db, current_user.id, days)
