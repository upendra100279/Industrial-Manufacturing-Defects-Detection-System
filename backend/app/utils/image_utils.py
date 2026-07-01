"""
OpenCV helpers for drawing YOLO bounding boxes, labels, and confidence
scores onto an image, then saving the annotated result.
"""
import cv2
import numpy as np

BOX_COLORS = [
    (0, 0, 255), (0, 165, 255), (0, 255, 255),
    (0, 255, 0), (255, 0, 0), (255, 0, 255),
]


def draw_detections(image: np.ndarray, detections: list[dict]) -> np.ndarray:
    annotated = image.copy()

    for i, det in enumerate(detections):
        color = BOX_COLORS[i % len(BOX_COLORS)]
        x1, y1, x2, y2 = map(int, [det["x_min"], det["y_min"], det["x_max"], det["y_max"]])

        cv2.rectangle(annotated, (x1, y1), (x2, y2), color, 2)

        label = f"{det['class_name']} {det['confidence']:.2f}"
        (text_w, text_h), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)

        cv2.rectangle(annotated, (x1, y1 - text_h - 8), (x1 + text_w + 4, y1), color, -1)
        cv2.putText(
            annotated, label, (x1 + 2, y1 - 4),
            cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA,
        )

    return annotated


def save_image(image: np.ndarray, path: str) -> None:
    cv2.imwrite(path, image)
