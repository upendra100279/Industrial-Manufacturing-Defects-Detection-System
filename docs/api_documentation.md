# API Documentation

Base URL: `/api`
Auth: `Authorization: Bearer <jwt>` on all protected routes (✅)

## Authentication

### POST /auth/register
Creates a new user account.
**Body:** `{ username, email, password, full_name? }`
**201:** UserResponse
**400:** `{ "detail": "Username or email already registered" }`

### POST /auth/login
**Body:** `{ username, password }`
**200:** `{ "access_token": "...", "token_type": "bearer" }`
**401:** `{ "detail": "Incorrect username or password" }`

### GET /auth/me ✅
**200:** UserResponse (current authenticated user)

## Detection

### POST /detect/image ✅
Multipart form-data, field: `file` (JPEG/PNG)
**200:** InspectionResponse with detections[] array

### GET /detect/result/{id}/image ✅
Returns the annotated JPEG as a file download.

## Video / Webcam

### POST /video/webcam-frame ✅
Multipart form-data, field: `file` (single JPEG frame)
**200:** raw annotated JPEG bytes — pipe directly into `<img src>`

### POST /video/upload ✅
Multipart form-data, field: `file` (mp4/avi/mov)
**200:** InspectionResponse aggregated across sampled frames

## History

### GET /history/ ✅
Query params: `skip`, `limit`, `defective_only`
**200:** `InspectionResponse[]`

### GET /history/{id} ✅
**200:** InspectionResponse with detections[]

### DELETE /history/{id} ✅
**204:** No content

## Analytics

### GET /analytics/dashboard ✅
**200:** `{ total_inspections, defective_count, non_defective_count, accuracy_rate, avg_confidence }`

### GET /analytics/defect-frequency ✅
**200:** `[{ class_name, count }]`

### GET /analytics/trend ✅
Query params: `days` (default 14, max 90)
**200:** `[{ date, total, defective }]`

## Error Format
All errors: `{ "detail": "<message>" }`
Validation errors (422): `{ "detail": "...", "errors": [...] }`
