"""
Trains a YOLOv8 defect detector on the converted MVTec AD dataset.
Wraps ultralytics' train() with our config file and saves best.pt to a
predictable location the backend can pick up.
"""
import shutil
import yaml
from pathlib import Path
from ultralytics import YOLO


def load_config(path: str = "../configs/train_config.yaml") -> dict:
    with open(path) as f:
        return yaml.safe_load(f)


def train_model(config_path: str = "../configs/train_config.yaml"):
    cfg = load_config(config_path)

    model = YOLO(cfg["model"]["base_weights"])

    results = model.train(
        data=cfg["dataset"]["data_yaml"],
        imgsz=cfg["model"]["image_size"],
        epochs=cfg["training"]["epochs"],
        batch=cfg["training"]["batch_size"],
        patience=cfg["training"]["patience"],
        lr0=cfg["training"]["lr0"],
        device=cfg["training"]["device"],
        project=cfg["training"]["project"],
        name=cfg["training"]["name"],
        hsv_h=cfg["augmentation"]["hsv_h"],
        hsv_s=cfg["augmentation"]["hsv_s"],
        hsv_v=cfg["augmentation"]["hsv_v"],
        fliplr=cfg["augmentation"]["fliplr"],
        mosaic=cfg["augmentation"]["mosaic"],
    )

    # Copy best.pt to backend's expected weights path
    run_dir = Path(cfg["training"]["project"]) / cfg["training"]["name"]
    best_weights = run_dir / "weights" / "best.pt"
    backend_weights_dir = Path("../../backend/storage/weights")
    backend_weights_dir.mkdir(parents=True, exist_ok=True)

    if best_weights.exists():
        shutil.copy(best_weights, backend_weights_dir / "best.pt")
        print(f"Copied trained weights to {backend_weights_dir / 'best.pt'}")
    else:
        print(f"Warning: best.pt not found at {best_weights}")

    return results


if __name__ == "__main__":
    train_model()
