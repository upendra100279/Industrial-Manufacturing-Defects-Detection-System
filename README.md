# 🏭 Industrial Defect Detection System

A production-style, full-stack AI application for real-time industrial
quality inspection — detects manufacturing defects from images, video,
and live webcam feeds using a custom-trained YOLOv8 model, with an
optional PatchCore anomaly-detection module for unsupervised defect
scoring and heatmap visualization.

![Status](https://img.shields.io/badge/status-active-success)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18-61dafb)
![License](https://img.shields.io/badge/license-MIT-blue)

---

## ✨ Features

- 🔐 JWT authentication with protected routes
- 📊 Analytics dashboard — inspection counts, defect trends, quality rate
- 🖼️ Drag-and-drop image upload with bounding-box + confidence visualization
- 🎥 Real-time webcam defect detection (frame-by-frame via backend inference)
- 📹 Video file upload with frame-by-frame sampling
- 📜 Paginated inspection history with filtering and detail modal
- 🌗 Dark/light theme toggle
- 🧠 Custom-trainable YOLOv8 model (MVTec AD or your own dataset)
- 🔬 Optional PatchCore anomaly detection + Grad-CAM heatmaps
- 🐳 Full Docker Compose deployment (PostgreSQL + FastAPI + React/Nginx)

---

## 🏗️ Tech Stack

| Layer       | Technology                                      |
|-------------|--------------------------------------------------|
| Frontend    | React 18, Vite, Tailwind CSS, Recharts, Axios   |
| Backend     | FastAPI, SQLAlchemy, python-jose (JWT)           |
| AI/ML       | YOLOv8 (Ultralytics), PyTorch, OpenCV           |
| Database    | PostgreSQL (prod) / SQLite (dev)                |
| Deployment  | Docker, Docker Compose, Nginx                   |

---

## 📁 Project Structure

```
industrial-defect-detection/
├── backend/          # FastAPI app (auth, detection, history, analytics)
├── frontend/         # React SPA (dashboard, detection, analytics, history)
├── ai-engine/        # YOLOv8 training pipeline + PatchCore module
├── docker/           # docker-compose.yml
└── docs/             # Architecture, API docs, system design
```

---

## 🚀 Quick Start

### Option A — Docker Compose (recommended, one command)

```bash
git clone <your-repo-url>
cd industrial-defect-detection

# Copy and configure environment
cp backend/.env.example backend/.env
# Edit backend/.env — set a strong SECRET_KEY

# Build and start all services
cd docker
docker compose up --build
```

| Service   | URL                          |
|-----------|------------------------------|
| Frontend  | http://localhost             |
| API       | http://localhost:8000        |
| API Docs  | http://localhost:8000/docs   |

---

### Option B — Local Development (no Docker)

#### Backend

```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY

# Run dev server
uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure API URL (optional — defaults to localhost:8000)
cp .env.example .env

# Start dev server
npm run dev
# → http://localhost:3000
```

---

## 🧠 Training Your Own Defect Detection Model

### 1. Get the MVTec AD Dataset

Download from https://www.mvtec.com/company/research/datasets/mvtec-ad
and place a category (e.g. `bottle`) under:

```
ai-engine/data/raw/mvtec_ad/bottle/
```

### 2. Convert masks → YOLO labels

```bash
cd ai-engine/src
python dataset.py \
  --mvtec_category_dir ../data/raw/mvtec_ad/bottle \
  --output_dir ../data/processed/mvtec_yolo
```

### 3. Train

```bash
python train.py
# Trained weights auto-copied to backend/storage/weights/best.pt
```

### 4. Validate & Evaluate

```bash
python validate.py   # mAP50, mAP50-95, Precision, Recall
python evaluate.py   # Per-class P/R/F1 + confusion_matrix.png
```

### 5. CLI Batch Inference (optional sanity check)

```bash
python infer.py \
  --weights ../../backend/storage/weights/best.pt \
  --source /path/to/test/images \
  --output ./inference_output
```

---

## 📡 API Reference

Interactive Swagger UI: `http://localhost:8000/docs`

| Method | Endpoint                          | Auth | Description                     |
|--------|-----------------------------------|------|---------------------------------|
| POST   | `/api/auth/register`              | —    | Create account                  |
| POST   | `/api/auth/login`                 | —    | Get JWT token                   |
| GET    | `/api/auth/me`                    | ✅   | Current user profile            |
| POST   | `/api/detect/image`               | ✅   | Image defect detection          |
| GET    | `/api/detect/result/{id}/image`   | ✅   | Download annotated image        |
| POST   | `/api/video/webcam-frame`         | ✅   | Single webcam frame detection   |
| POST   | `/api/video/upload`               | ✅   | Video file detection            |
| GET    | `/api/history/`                   | ✅   | List inspection history         |
| GET    | `/api/history/{id}`               | ✅   | Inspection detail               |
| DELETE | `/api/history/{id}`               | ✅   | Delete inspection               |
| GET    | `/api/analytics/dashboard`        | ✅   | Dashboard stats                 |
| GET    | `/api/analytics/defect-frequency` | ✅   | Defect count by class           |
| GET    | `/api/analytics/trend`            | ✅   | Daily inspection trend          |

---

## 🧪 Running Tests

```bash
cd backend
pytest tests/ -v
```

Tests cover: user registration, login, auth guards, analytics empty-state,
detection endpoint content-type validation.

---

## 🗄️ Database Schema

```
users          — id, username, email, hashed_password, full_name, is_active, created_at
inspections    — id, user_id(FK), source_type, original_filename,
                 processed_image_path, is_defective, defect_count,
                 avg_confidence, created_at
detections     — id, inspection_id(FK), class_name, confidence,
                 x_min, y_min, x_max, y_max
```

Indexes on `users.username`, `users.email`, and `inspections.user_id`
keep auth lookups and history pagination fast at scale.

---

## 🐳 Production Deployment Notes

- Set a strong random `SECRET_KEY` (32+ chars) in `backend/.env`
- Backend storage volume (`backend_storage`) persists uploaded and
  processed images across container restarts
- PostgreSQL data is persisted in the `pgdata` named volume
- To use a GPU for inference: add `deploy.resources.reservations.devices`
  to the `backend` service in `docker-compose.yml` and ensure
  `nvidia-container-toolkit` is installed on the host

---

## 📄 License

MIT — free for personal and commercial use.
