# Awesome 1ntelligence
# Ultralytics YOLOv8 Basics
# Author: Abdullah As-Sadeed (@bitscoper)

from pathlib import Path
from ultralytics import YOLO
import glob
import os
import sys

if __name__ == "__main__":
    file_path = Path(__file__).resolve()
    root_path = file_path.parent

    if root_path not in sys.path:
        sys.path.append(str(root_path))

    ROOT = root_path.relative_to(Path.cwd())

    directory = ROOT / "YOLOv8_Official_Models"

    if not os.path.exists(directory):
        os.makedirs(directory)

    YOLOv8_official_models = glob.glob(str(directory) + "/*")

    for YOLO_official_model in YOLOv8_official_models:
        os.remove(YOLO_official_model)
        print(f"Deleted {YOLO_official_model}")

    YOLO_model_type_suffixes = ["", "-seg", "-pose"]
    YOLO_model_weight_suffixes = ["n", "s", "m", "l", "x"]

    for YOLO_model_type_suffix in YOLO_model_type_suffixes:
        for YOLO_model_weight_suffix in YOLO_model_weight_suffixes:
            YOLO_model_path = (
                str(directory)
                + "/yolov8"
                + YOLO_model_weight_suffix
                + YOLO_model_type_suffix
                + ".pt"
            )

            try:
                YOLO_model = YOLO(YOLO_model_path)

            except Exception as exception:
                print(f"Error downloading YOLOv8 model {YOLO_model_path}: {exception}")
