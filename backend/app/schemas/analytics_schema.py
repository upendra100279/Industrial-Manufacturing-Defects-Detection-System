"""
Schemas for dashboard/analytics aggregate responses.
"""
from pydantic import BaseModel


class DashboardStats(BaseModel):
    total_inspections: int
    defective_count: int
    non_defective_count: int
    accuracy_rate: float
    avg_confidence: float


class DefectFrequencyItem(BaseModel):
    class_name: str
    count: int


class TrendPoint(BaseModel):
    date: str
    total: int
    defective: int
