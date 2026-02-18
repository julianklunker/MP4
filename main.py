import cv2
import numpy as np
from Camera.Camera import Camera
from Data_analysis.Tracker import Tracker


camera = Camera(camera_index=0)
camera.connect()

tracker = Tracker()

if __name__ == "__main__":
    while True:
        frame = camera.capture_frame()
        object_information = tracker.object_information(frame)
        cv2.imshow("Camera Feed", frame)
        if frame is not None:
            if object_information:
                print(f"{object_information}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
          break