"""
Aggregation queries for the dashboard and analytics pages.
"""
from sqlalchemy.orm import Session
from sqlalchemy import func, cast, Integer
from datetime import datetime, timedelta

from app.models.inspection import Inspection
from app.models.detection import Detection
from app.schemas.analytics_schema import DashboardStats, DefectFrequencyItem, TrendPoint


def get_dashboard_stats(db: Session, user_id: int) -> DashboardStats:
    total = db.query(func.count(Inspection.id)).filter(
        Inspection.user_id == user_id
    ).scalar() or 0

    defective = db.query(func.count(Inspection.id)).filter(
        Inspection.user_id == user_id,
        Inspection.is_defective == True
    ).scalar() or 0

    non_defective = total - defective

    avg_conf = db.query(func.avg(Inspection.avg_confidence)).filter(
        Inspection.user_id == user_id
    ).scalar() or 0.0

    accuracy_rate = (non_defective / total * 100) if total > 0 else 0.0

    return DashboardStats(
        total_inspections=total,
        defective_count=defective,
        non_defective_count=non_defective,
        accuracy_rate=round(accuracy_rate, 2),
        avg_confidence=round(float(avg_conf), 4),
    )


def get_defect_frequency(db: Session, user_id: int) -> list[DefectFrequencyItem]:
    rows = (
        db.query(
            Detection.class_name,
            func.count(Detection.id).label("count")
        )
        .join(Inspection, Inspection.id == Detection.inspection_id)
        .filter(Inspection.user_id == user_id)
        .group_by(Detection.class_name)
        .order_by(func.count(Detection.id).desc())
        .all()
    )
    return [DefectFrequencyItem(class_name=r[0], count=r[1]) for r in rows]


def get_trend(db: Session, user_id: int, days: int = 14) -> list[TrendPoint]:
    since = datetime.utcnow() - timedelta(days=days)

    rows = (
        db.query(
            func.date(Inspection.created_at).label("day"),
            func.count(Inspection.id).label("total"),
            func.sum(cast(Inspection.is_defective, Integer)).label("defective"),
        )
        .filter(
            Inspection.user_id == user_id,
            Inspection.created_at >= since
        )
        .group_by(func.date(Inspection.created_at))
        .order_by(func.date(Inspection.created_at))
        .all()
    )

    return [
        TrendPoint(
            date=str(r.day),
            total=r.total,
            defective=int(r.defective or 0)
        )
        for r in rows
    ]