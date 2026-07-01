"""
FastAPI application entrypoint.
Wires together middleware, routers, and startup/shutdown events.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.core.config import settings
from app.core.logging_config import logger
from app.db.base import Base, engine
from app.middleware.error_handler import register_error_handlers
from app.routes import auth_routes, detection_routes, video_routes, history_routes, analytics_routes


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting up Industrial Defect Detection System...")
    Base.metadata.create_all(bind=engine)

    from app.services.yolo_service import yolo_service
    yolo_service.load_model()

    yield

    logger.info("Shutting down...")


app = FastAPI(
    title=settings.APP_NAME,
    description="Production-grade Industrial Defect Detection API powered by YOLOv8",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_error_handlers(app)

app.include_router(auth_routes.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(detection_routes.router, prefix="/api/detect", tags=["Detection"])
app.include_router(video_routes.router, prefix="/api/video", tags=["Video/Webcam"])
app.include_router(history_routes.router, prefix="/api/history", tags=["History"])
app.include_router(analytics_routes.router, prefix="/api/analytics", tags=["Analytics"])


@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "ok", "service": settings.APP_NAME}
