# System Design

## Scaling Considerations

### Current (single-server) design
- YOLOv8 model loaded as a process-level singleton
- SQLite fine for development; swap DATABASE_URL for PostgreSQL in prod
- File storage on local disk under storage/

### Path to production scale
1. **GPU inference workers** — move model.predict() calls to a Celery
   task queue backed by Redis, with GPU-enabled worker containers.
   The API server enqueues jobs and polls for results.
2. **Object storage** — replace local storage/ with S3/GCS for
   multi-instance deployments where each container needs image access.
3. **Analytics caching** — add Redis cache on /analytics/dashboard
   aggregates (TTL 60s). Dashboard stats are read-heavy and don't need
   per-request freshness.
4. **Horizontal API scaling** — JWT is stateless so the backend scales
   behind a load balancer with no sticky sessions required.

## Security Notes
- Passwords hashed with bcrypt (passlib)
- JWT signed with HS256; secret key must be ≥32 random chars in prod
- File uploads validated by content-type before processing
- All DB queries parameterized via SQLAlchemy ORM (no raw SQL)
- CORS restricted to configured ALLOWED_ORIGINS

## Trade-offs Made
- Webcam uses polling (POST every 800ms) instead of WebSockets for
  simplicity. WebSocket upgrade would reduce latency from ~800ms to
  ~100-200ms for a smoother live feed.
- Video files are sampled (every 10th frame) rather than processed
  frame-by-frame to keep upload response times reasonable.
- PatchCore and Grad-CAM are implemented as standalone modules rather
  than integrated into the main detection route — reduces complexity
  while keeping the code demonstrable.
