"""
Inspection ORM model — one row per uploaded image/video frame analyzed.
"""
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base


class Inspection(Base):
    __tablename__ = "inspections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    source_type = Column(String(20), default="image")
    original_filename = Column(String(255), nullable=True)
    processed_image_path = Column(String(255), nullable=True)

    is_defective = Column(Boolean, default=False)
    defect_count = Column(Integer, default=0)
    avg_confidence = Column(Float, default=0.0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    owner = relationship("User", back_populates="inspections")
    detections = relationship("Detection", back_populates="inspection", cascade="all, delete-orphan")
