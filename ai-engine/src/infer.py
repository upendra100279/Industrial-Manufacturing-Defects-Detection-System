"""
Standalone CLI inference script — useful for quick sanity checks outside
the API, or for batch-processing a folder of images.
"""
import argparse
from pathlib import Path
import cv2
from ultralytics import YOLO


def run_inference(weights_path: str, source_dir: str, output_dir: str, conf: float = 0.4):
    model = YOLO(weights_path)
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    results = model.predict(source=source_dir, conf=conf, save=False, verbose=False)

    for result in results:
        img = result.orig_img.copy()
        for box in result.boxes:
            x1, y1, x2, y2 = map(int, box.xyxy[0].tolist())
            cls_name = result.names[int(box.cls[0])]
            conf_score = float(box.conf[0])
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 0, 255), 2)
            cv2.putText(img, f"{cls_name} {conf_score:.2f}", (x1, y1 - 8),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        out_path = Path(output_dir) / Path(result.path).name
        cv2.imwrite(str(out_path), img)
        print(f"Saved: {out_path} ({len(result.boxes)} defects)")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--weights", required=True)
    parser.add_argument("--source", required=True, help="folder of images")
    parser.add_argument("--output", default="./inference_output")
    parser.add_argument("--conf", type=float, default=0.4)
    args = parser.parse_args()
    run_inference(args.weights, args.source, args.output, args.conf)
