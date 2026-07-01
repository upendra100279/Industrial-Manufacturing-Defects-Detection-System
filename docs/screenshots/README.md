# 📸 Screenshots

A visual walkthrough of the **Industrial Defect Detection System** — from login to live defect inspection results.

> Place these images in this `screenshots/` folder using the filenames below (rename as needed), then this README will render them correctly on GitHub.

---

## 🔐 Authentication

**Login / Sign In**
JWT-secured sign-in screen for the inspection dashboard.

![Login screen](./01-login.png)

---

## 📊 Dashboard

Overview of inspection stats — total inspections, defective vs. non-defective counts, quality rate, inspection trend over time, and defect frequency by type.

![Dashboard overview](./02-dashboard.png)

---

## 🖼️ Defect Detection — Image Upload

**Empty state** — drag-and-drop upload zone for product images (JPEG/PNG, up to 10MB), with a Live Webcam tab for real-time detection.

![Detection page - empty state](./03-detection-empty.png)

**Image uploaded**, ready to run inference.

![Detection page - image uploaded](./04-detection-uploaded.png)

**Detection result** — bounding box drawn around the identified defect (`casting_defect`) with a confidence score, plus a download option for the annotated image.

![Detection result with bounding box](./05-detection-result.png)

---

## 📈 Analytics

Deeper defect analytics with configurable time ranges (7/14/30/90 days) — inspection trend line chart and defect count broken down by product/defect type.

![Analytics page](./06-analytics.png)

---

## 🕓 Inspection History

Paginated, filterable log of past inspections showing status (Pass/Defective), defect count, confidence score, and timestamp for each run, with view/delete actions.

![Inspection history table](./07-history.png)

---

### 🗂️ Suggested filenames

| # | Screenshot | Suggested filename |
|---|------------|---------------------|
| 1 | Login page | `01-login.png` |
| 2 | Dashboard | `02-dashboard.png` |
| 3 | Detection (empty state) | `03-detection-empty.png` |
| 4 | Detection (image uploaded) | `04-detection-uploaded.png` |
| 5 | Detection (result with bounding box) | `05-detection-result.png` |
| 6 | Analytics | `06-analytics.png` |
| 7 | Inspection history | `07-history.png` |
