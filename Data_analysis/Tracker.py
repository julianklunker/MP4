import cv2
import numpy as np
from Camera.Camera import Camera

class Tracker:
    def __init__ (self):
        self.object_position = None
        self.object_color = None
        

    def object_information(self, frame):
        target_colors = {
            "Red": [np.array([0, 100, 70]), np.array([20, 255, 255]), (0, 0, 255)],
            "Green": [np.array([40, 100, 70]), np.array([80, 255, 255]), (0, 255, 0)],
        }
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        for color_name, (lower, upper, draw_color) in target_colors.items():
            mask = cv2.inRange(hsv_frame, lower, upper)
            mask = cv2.dilate(mask, None, iterations=1)

            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 800:
                    x, y, w, h = cv2.boundingRect(cnt)
                    object_x = x + w // 2
                    cy = y + h // 2
                    return (object_x, color_name)
        

    
    