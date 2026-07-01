# Architecture Overview

## System Diagram

```
┌─────────────────────────────────────────────────────────────┐
│                      CLIENT (Browser)                        │
│   React SPA — Dashboard / Detection / Analytics / History   │
└────────────────────────┬────────────────────────────────────┘
                         │ REST (Axios) + JWT Bearer
┌────────────────────────▼────────────────────────────────────┐
│                     FASTAPI BACKEND                          │
│  routes/ · services/ · models/ · schemas/ · middleware/      │
│  auth · detect · video · history · analytics                 │
└────────────────────────┬────────────────────────────────────┘
                         │ loads weights / runs inference
┌────────────────────────▼────────────────────────────────────┐
│                    AI ENGINE (PyTorch)                        │
│  YOLOv8 · OpenCV · PatchCore anomaly · Grad-CAM heatmaps   │
└────────────────────────┬────────────────────────────────────┘
                         │
┌────────────────────────▼────────────────────────────────────┐
│         PostgreSQL / SQLite + File Storage                    │
│  users · inspections · detections                            │
│  storage/uploads · storage/processed · storage/weights       │
└─────────────────────────────────────────────────────────────┘
```

## Key Design Decisions

1. **Model singleton + thread-pool inference** — YOLO weights load once
   at startup. Blocking inference runs in `run_in_executor` so it
   never stalls the async FastAPI event loop.

2. **AI engine decoupled from API** — `ai-engine/` is independently
   testable and could be swapped for Triton/TorchServe without touching
   route code.

3. **Webcam frames not persisted** — only explicit "capture" actions
   write to the DB, preventing the database from filling with hundreds
   of rows per minute during live monitoring.

4. **Stateless JWT auth** — horizontally scalable without sticky
   sessions or a shared session store.

5. **PostgreSQL in prod, SQLite in dev** — same SQLAlchemy models
   work for both via a single DATABASE_URL env var swap.
