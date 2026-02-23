import cv2
import numpy as np

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        # Get the color of the pixel at (x, y)
        # Note: OpenCV uses (row, col) which is (y, x)
        pixel_bgr = frame[y, x]
        
        # Convert that single pixel to HSV
        # We put it in a 1x1 image array because cvtColor expects an image
        pixel_node = np.uint8([[pixel_bgr]])
        pixel_hsv = cv2.cvtColor(pixel_node, cv2.COLOR_BGR2HSV)[0][0]
        
        h, s, v = pixel_hsv
        
        print(f"Coordinates: ({x}, {y}) | HSV: {h}, {s}, {v}")

        # Draw on the frame
        font = cv2.FONT_HERSHEY_SIMPLEX
        str_hsv = f'H:{h} S:{s} V:{v}'
        cv2.putText(frame, str_hsv, (x, y), font, 0.5, (255, 255, 255), 1)
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
        cv2.imshow('HSV Picker', frame)

# Setup Camera
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
cv2.namedWindow('HSV Picker')
cv2.setMouseCallback('HSV Picker', click_event)

print("Click to see HSV values. Press 'q' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    cv2.imshow('HSV Picker', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()