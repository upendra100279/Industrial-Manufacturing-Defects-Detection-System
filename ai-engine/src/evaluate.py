"""
Detailed evaluation beyond ultralytics' defaults: builds a confusion
matrix and per-class precision/recall/F1 table by comparing predicted
boxes against ground-truth labels at a fixed IoU threshold.
"""
import argparse
from pathlib import Path
import yaml
from ultralytics import YOLO
from sklearn.metrics import confusion_matrix, classification_report
import matplotlib.pyplot as plt


def iou(box_a, box_b):
    xa1, ya1, xa2, ya2 = box_a
    xb1, yb1, xb2, yb2 = box_b

    inter_x1, inter_y1 = max(xa1, xb1), max(ya1, yb1)
    inter_x2, inter_y2 = min(xa2, xb2), min(ya2, yb2)
    inter_area = max(0, inter_x2 - inter_x1) * max(0, inter_y2 - inter_y1)

    area_a = (xa2 - xa1) * (ya2 - ya1)
    area_b = (xb2 - xb1) * (yb2 - yb1)
    union = area_a + area_b - inter_area

    return inter_area / union if union > 0 else 0.0


def load_yolo_label(label_path: Path, img_w: int, img_h: int) -> list[tuple[int, tuple]]:
    """Reads a YOLO .txt label file, returns [(class_id, (x1,y1,x2,y2)), ...]."""
    if not label_path.exists():
        return []
    boxes = []
    for line in label_path.read_text().strip().splitlines():
        if not line:
            continue
        cls, cx, cy, w, h = map(float, line.split())
        x1 = (cx - w / 2) * img_w
        y1 = (cy - h / 2) * img_h
        x2 = (cx + w / 2) * img_w
        y2 = (cy + h / 2) * img_h
        boxes.append((int(cls), (x1, y1, x2, y2)))
    return boxes


def evaluate(weights_path: str, data_yaml: str, iou_threshold: float = 0.5):
    with open(data_yaml) as f:
        data_cfg = yaml.safe_load(f)

    class_names = data_cfg["names"]
    val_img_dir = Path(data_cfg["path"]) / "images/val"
    val_lbl_dir = Path(data_cfg["path"]) / "labels/val"

    model = YOLO(weights_path)

    y_true, y_pred = [], []

    for img_path in sorted(val_img_dir.glob("*.jpg")):
        result = model.predict(source=str(img_path), verbose=False)[0]
        img_h, img_w = result.orig_shape

        gt_boxes = load_yolo_label(val_lbl_dir / f"{img_path.stem}.txt", img_w, img_h)
        pred_boxes = [
            (int(box.cls[0]), tuple(box.xyxy[0].tolist()))
            for box in result.boxes
        ]

        matched_gt = set()
        for pred_cls, pred_box in pred_boxes:
            best_iou, best_gt_idx, best_gt_cls = 0, -1, None
            for idx, (gt_cls, gt_box) in enumerate(gt_boxes):
                if idx in matched_gt:
                    continue
                score = iou(pred_box, gt_box)
                if score > best_iou:
                    best_iou, best_gt_idx, best_gt_cls = score, idx, gt_cls

            if best_iou >= iou_threshold:
                matched_gt.add(best_gt_idx)
                y_true.append(best_gt_cls)
                y_pred.append(pred_cls)
            else:
                y_true.append(len(class_names))  # "background" — false positive
                y_pred.append(pred_cls)

        for idx, (gt_cls, _) in enumerate(gt_boxes):
            if idx not in matched_gt:
                y_true.append(gt_cls)
                y_pred.append(len(class_names))  # missed detection (false negative)

    labels = list(range(len(class_names) + 1))
    display_names = list(class_names.values()) + ["background"]

    cm = confusion_matrix(y_true, y_pred, labels=labels)
    report = classification_report(y_true, y_pred, labels=labels, target_names=display_names)

    print("\n=== Classification Report (P/R/F1) ===")
    print(report)

    fig, ax = plt.subplots(figsize=(8, 6))
    im = ax.imshow(cm, cmap="Blues")
    ax.set_xticks(range(len(display_names)))
    ax.set_yticks(range(len(display_names)))
    ax.set_xticklabels(display_names, rotation=45, ha="right")
    ax.set_yticklabels(display_names)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Ground Truth")
    ax.set_title("Defect Detection Confusion Matrix")
    for i in range(len(display_names)):
        for j in range(len(display_names)):
            ax.text(j, i, cm[i, j], ha="center", va="center", color="black")
    fig.colorbar(im)
    plt.tight_layout()
    plt.savefig("confusion_matrix.png", dpi=150)
    print("\nConfusion matrix saved to confusion_matrix.png")

    return report, cm


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", default="../runs/defect_detector_v1/weights/best.pt")
    parser.add_argument("--data", default="../data/processed/mvtec_yolo/data.yaml")
    args = parser.parse_args()
    evaluate(args.weights, args.data)
