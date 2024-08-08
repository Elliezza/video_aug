import os
import cv2
import math
def get_video_duration(file_path):
    cap = cv2.VideoCapture(file_path)
    fps = cap.get(cv2.CAP_PROP_FPS)  # Frames per second
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Total number of frames
    duration = frame_count / fps  # Duration in seconds
    cap.release()
    return math.ceil(duration)

# Function to get file size
def get_file_size(file_path):
    return math.ceil(os.path.getsize(file_path) / 1024)  # Size in KB

