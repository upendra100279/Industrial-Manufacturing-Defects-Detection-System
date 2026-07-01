"""
Converts MVTec AD's pixel-level ground-truth masks into YOLO-format
bounding-box labels, and builds the data.yaml YOLO expects.

MVTec AD directory layout (per category, e.g. "bottle"):
    bottle/train/good/*.png
    bottle/test/{defect_type}/*.png
    bottle/ground_truth/{defect_type}/*_mask.png

Output layout (YOLO):
    mvtec_yolo/images/train/*.jpg
    mvtec_yolo/images/val/*.jpg
    mvtec_yolo/labels/train/*.txt
    mvtec_yolo/labels/val/*.txt
    mvtec_yolo/data.yaml
"""
import shutil
import cv2
import numpy as np
import yaml
from pathlib import Path


def mask_to_bboxes(mask_path: str, min_area: int = 20) -> list[tuple[int, int, int, int]]:
    """Extracts bounding boxes from a binary defect mask via contour detection."""
    mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
    if mask is None:
        return []

    _, binary = cv2.threshold(mask, 127, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    boxes = []
    for c in contours:
        area = cv2.contourArea(c)
        if area < min_area:
            continue
        x, y, w, h = cv2.boundingRect(c)
        boxes.append((x, y, x + w, y + h))
    return boxes


def to_yolo_format(box, img_w, img_h):
    """Converts (x1,y1,x2,y2) pixel box to YOLO's normalized (cx,cy,w,h)."""
    x1, y1, x2, y2 = box
    cx = (x1 + x2) / 2 / img_w
    cy = (y1 + y2) / 2 / img_h
    w = (x2 - x1) / img_w
    h = (y2 - y1) / img_h
    return cx, cy, w, h


def build_yolo_dataset(mvtec_category_dir: str, output_dir: str, val_split: float = 0.2):
    """
    Walks one MVTec AD category folder, converts defective test images +
    masks into YOLO image/label pairs, and writes data.yaml.
    'good' (non-defective) test images are included as background-only
    examples (empty label files) so the model learns the non-defective class.
    """
    category_name = Path(mvtec_category_dir).name
    img_train_dir = Path(output_dir) / "images/train"
    img_val_dir = Path(output_dir) / "images/val"
    lbl_train_dir = Path(output_dir) / "labels/train"
    lbl_val_dir = Path(output_dir) / "labels/val"
    for d in [img_train_dir, img_val_dir, lbl_train_dir, lbl_val_dir]:
        d.mkdir(parents=True, exist_ok=True)

    test_dir = Path(mvtec_category_dir) / "test"
    gt_dir = Path(mvtec_category_dir) / "ground_truth"

    defect_types = sorted([d.name for d in test_dir.iterdir() if d.is_dir() and d.name != "good"])
    class_map = {name: idx for idx, name in enumerate(defect_types)}

    samples = []  # (image_path, label_lines)

    # Defective samples — boxes from masks
    for defect_type in defect_types:
        defect_img_dir = test_dir / defect_type
        defect_mask_dir = gt_dir / defect_type
        for img_path in sorted(defect_img_dir.glob("*.png")):
            mask_path = defect_mask_dir / f"{img_path.stem}_mask.png"
            if not mask_path.exists():
                continue

            img = cv2.imread(str(img_path))
            h, w = img.shape[:2]
            boxes = mask_to_bboxes(str(mask_path))
            if not boxes:
                continue

            lines = []
            for box in boxes:
                cx, cy, bw, bh = to_yolo_format(box, w, h)
                lines.append(f"{class_map[defect_type]} {cx:.6f} {cy:.6f} {bw:.6f} {bh:.6f}")

            samples.append((str(img_path), lines))

    # Good (non-defective) samples — empty labels, teaches the model
    # what a clean product looks like
    good_dir = test_dir / "good"
    if good_dir.exists():
        for img_path in sorted(good_dir.glob("*.png")):
            samples.append((str(img_path), []))

    # Train/val split
    np.random.seed(42)
    np.random.shuffle(samples)
    split_idx = int(len(samples) * (1 - val_split))
    train_samples, val_samples = samples[:split_idx], samples[split_idx:]

    def write_split(samples, img_dir, lbl_dir):
        for img_path, lines in samples:
            stem = Path(img_path).stem + f"_{category_name}"
            shutil.copy(img_path, img_dir / f"{stem}.jpg")
            with open(lbl_dir / f"{stem}.txt", "w") as f:
                f.write("\n".join(lines))

    write_split(train_samples, img_train_dir, lbl_train_dir)
    write_split(val_samples, img_val_dir, lbl_val_dir)

    data_yaml = {
        "path": str(Path(output_dir).resolve()),
        "train": "images/train",
        "val": "images/val",
        "names": {v: k for k, v in class_map.items()},
    }
    with open(Path(output_dir) / "data.yaml", "w") as f:
        yaml.dump(data_yaml, f, sort_keys=False)

    print(f"Built YOLO dataset for '{category_name}': "
          f"{len(train_samples)} train / {len(val_samples)} val samples, "
          f"{len(class_map)} defect classes: {list(class_map.keys())}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--mvtec_category_dir", required=True,
                         help="e.g. data/raw/mvtec_ad/bottle")
    parser.add_argument("--output_dir", default="../data/processed/mvtec_yolo")
    args = parser.parse_args()
    build_yolo_dataset(args.mvtec_category_dir, args.output_dir)
