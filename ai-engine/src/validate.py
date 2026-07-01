"""
Runs YOLOv8's built-in validation loop on the val split and prints
standard detection metrics (mAP50, mAP50-95, precision, recall).
"""
import argparse
from ultralytics import YOLO


def validate_model(weights_path: str, data_yaml: str):
    model = YOLO(weights_path)
    metrics = model.val(data=data_yaml)

    print("\n=== Validation Metrics ===")
    print(f"mAP50:    {metrics.box.map50:.4f}")
    print(f"mAP50-95: {metrics.box.map:.4f}")
    print(f"Precision: {metrics.box.mp:.4f}")
    print(f"Recall:    {metrics.box.mr:.4f}")
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", default="../runs/defect_detector_v1/weights/best.pt")
    parser.add_argument("--data", default="../data/processed/mvtec_yolo/data.yaml")
    args = parser.parse_args()
    validate_model(args.weights, args.data)
