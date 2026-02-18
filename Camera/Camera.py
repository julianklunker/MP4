import cv2
import numpy as np

class Camera:
    def __init__(self, camera_index=0):
        self.camera_index = camera_index
        self.cap = None
    
    def connect(self):
        self.cap = cv2.VideoCapture(self.camera_index)
        if not not self.cap.isOpened():
            print(f"Error: Could not open camera with index {self.camera_index}.")
            return False
    
    def capture_frame(self):
        if self.cap is None:
            print("Error: Camera not connected.")
            return None
        ret, frame = self.cap.read()
        if not ret:
            print("Error: Could not read frame from camera.")
            return None
        return frame

    def show_feed(self):
        frame = self.capture_frame()
        cv2.imshow("Camera Feed", frame)
