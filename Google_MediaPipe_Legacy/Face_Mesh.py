# By Abdullah As-Sadeed

from pathlib import Path
from tkinter import messagebox
import cv2 as opencv
import mediapipe as mp
import sys

sys.path.append(str(Path(__file__).resolve().parents[1]))
from Common import *

if __name__ == "__main__":
    mp_drawing_utils = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_face_mesh = mp.solutions.face_mesh

    IMAGE_FILE_INPUT = "Image File"
    VIDEO_FILE_INPUT = "Video File"
    WEBCAM_INPUT = "Webcam"
    RTSP_INPUT = "RTSP"
    INPUT_MODES = [IMAGE_FILE_INPUT, VIDEO_FILE_INPUT, WEBCAM_INPUT, RTSP_INPUT]

    DEFAULT_DETECTION_CONFIDENCE = 50
    DEFAULT_TRACKING_CONFIDENCE = 50

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

    detection_confidence = (
        select_number("Set Detection Confidence", 0, 100, DEFAULT_DETECTION_CONFIDENCE)
        / 100
    )
    tracking_confidence = (
        select_number("Set Tracking Confidence", 0, 100, DEFAULT_TRACKING_CONFIDENCE)
        / 100
    )

    def process(frame):
        with mp_face_mesh.FaceMesh(
            refine_landmarks=True,
            min_detection_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence,
        ) as face_mesh:
            frame.flags.writeable = False
            frame = opencv.cvtColor(frame, opencv.COLOR_BGR2RGB)

            results = face_mesh.process(frame)

            frame.flags.writeable = True
            frame = opencv.cvtColor(frame, opencv.COLOR_RGB2BGR)

            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:
                    mp_drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                    )
                    mp_drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
                    )
                    mp_drawing_utils.draw_landmarks(
                        image=frame,
                        landmark_list=face_landmarks,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
                    )

            opencv.imshow("MediaPipe Face Mesh", frame)

    def process_in_loop(input):
        try:
            capture = opencv.VideoCapture(input)

            while capture.isOpened():
                success, frame = capture.read()

                if success:
                    process(frame)
                    opencv.waitKey(1)

                else:
                    capture.release()
                    break

        except Exception as error:
            messagebox.showerror("Error", f"Error: {error}")
            sys.exit(1)

    if input_mode == IMAGE_FILE_INPUT:
        image = opencv.imread(file)
        process(image)

    elif input_mode == VIDEO_FILE_INPUT:
        process_in_loop(file)

    elif input_mode == WEBCAM_INPUT:
        process_in_loop(webcam_index)

    elif input_mode == RTSP_INPUT:
        process_in_loop(rtsp_url)

    opencv.waitKey(0)

    opencv.destroyAllWindows()

sys.exit(0)
