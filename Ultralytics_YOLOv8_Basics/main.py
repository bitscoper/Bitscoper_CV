# By Abdullah As-Sadeed

from pathlib import Path
from tkinter import messagebox
from ultralytics import YOLO
import cv2 as opencv
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from Common import *

if __name__ == "__main__":
    IMAGE_FILE_INPUT = "Image File"
    VIDEO_FILE_INPUT = "Video File"
    WEBCAM_INPUT = "Webcam"
    RTSP_INPUT = "RTSP"
    INPUT_MODES = [IMAGE_FILE_INPUT, VIDEO_FILE_INPUT, WEBCAM_INPUT, RTSP_INPUT]

    OBJECT_DETECTION = "Object Detection"
    OBJECT_SEGMENTATION = "Object Segmentation"
    POSE_DETECTION = "Pose Detection"
    MODEL_TYPES = [OBJECT_DETECTION, OBJECT_SEGMENTATION, POSE_DETECTION]

    NANO_MODEL_WEIGHT = "Nano"
    SMALL_MODEL_WEIGHT = "Small"
    MEDIUM_MODEL_WEIGHT = "Medium"
    LARGE_MODEL_WEIGHT = "Large"
    EXTRA_LARGE_MODEL_WEIGHT = "Extra Large"
    MODEL_WEIGHTS = [
        NANO_MODEL_WEIGHT,
        SMALL_MODEL_WEIGHT,
        MEDIUM_MODEL_WEIGHT,
        LARGE_MODEL_WEIGHT,
        EXTRA_LARGE_MODEL_WEIGHT,
    ]

    TRACKERS = ["bytetrack.yaml", "botsort.yaml", "None"]

    DEFAULT_CONFIDENCE = 40

    input_mode = select_option("Select Input Mode", INPUT_MODES)

    if input_mode == IMAGE_FILE_INPUT or input_mode == VIDEO_FILE_INPUT:
        file = select_directory_or_file("File")

    elif input_mode == WEBCAM_INPUT:
        webcam_index = int(enter_text("Enter Webcam Index", "0"))

    elif input_mode == RTSP_INPUT:
        rtsp_url = enter_text(
            "Enter RTSP URL", "rtsp://username:password@ip_address:port/"
        )

    else:
        messagebox.showerror("Error", "Could not determine input mode!")
        sys.exit(1)

    model_type = select_option("Select Model Type", MODEL_TYPES)

    if model_type == OBJECT_DETECTION:
        model_type_suffix = ""
    elif model_type == OBJECT_SEGMENTATION:
        model_type_suffix = "-seg"
    elif model_type == POSE_DETECTION:
        model_type_suffix = "-pose"
    else:
        messagebox.showerror("Error", "Could not determine model type!")
        sys.exit(1)

    model_weight = select_option("Select Model Weight", MODEL_WEIGHTS)

    if model_weight == NANO_MODEL_WEIGHT:
        model_weight_suffix = "n"
    elif model_weight == SMALL_MODEL_WEIGHT:
        model_weight_suffix = "s"
    elif model_weight == MEDIUM_MODEL_WEIGHT:
        model_weight_suffix = "m"
    elif model_weight == LARGE_MODEL_WEIGHT:
        model_weight_suffix = "l"
    elif model_weight == EXTRA_LARGE_MODEL_WEIGHT:
        model_weight_suffix = "x"
    else:
        messagebox.showerror("Error", "Could not determine model weight!")
        sys.exit(1)

    tracker = select_option("Select Tracker", TRACKERS)

    confidence = select_number("Set Confidence", 0, 100, DEFAULT_CONFIDENCE) / 100

    model_path = (
        "YOLOv8_Official_Models/" + f"yolov8{model_weight_suffix}{model_type_suffix}.pt"
    )

    try:
        model = YOLO(model_path)

    except Exception as error:
        messagebox.showerror("Error", f"Error: {error}")
        sys.exit(1)

    def process(input):
        if model_type == OBJECT_SEGMENTATION:
            if tracker == "None":
                model.predict(input, conf=confidence, retina_masks=True, show=True)

            else:
                model.track(
                    input,
                    conf=confidence,
                    tracker=tracker,
                    persist=True,
                    retina_masks=True,
                    show=True,
                )

        else:
            if tracker == "None":
                model.predict(input, conf=confidence, show=True)

            else:
                model.track(
                    input,
                    conf=confidence,
                    tracker=tracker,
                    persist=True,
                    show=True,
                )

    def process_in_loop(input):
        try:
            capture = opencv.VideoCapture(input)

            while capture.isOpened():
                success, frame = capture.read()

                if success:
                    process(frame)

                else:
                    capture.release()
                    break

        except Exception as error:
            messagebox.showerror("Error", f"Error: {error}")
            sys.exit(1)

    if input_mode == IMAGE_FILE_INPUT or input_mode == VIDEO_FILE_INPUT:
        process(file)

    elif input_mode == WEBCAM_INPUT:
        process_in_loop(webcam_index)

    elif input_mode == RTSP_INPUT:
        process_in_loop(rtsp_url)

    opencv.waitKey(0)

    opencv.destroyAllWindows()

sys.exit(0)
