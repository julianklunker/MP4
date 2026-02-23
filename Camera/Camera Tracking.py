import cv2
import numpy as np

video = cv2.VideoCapture(1)

# Check if camera opened at all
if not video.isOpened():
    print("Error: Could not open webcam.")
    exit()

# 1. Define our "Library" of colors (HSV ranges)
# Format: "ColorName": [Lower_Bound, Upper_Bound, Display_BGR_Color]
color_library = {
    #"Green": [np.array([35, 100, 100]), np.array([85, 255, 255]), (0, 255, 0)],
    #"Blue":  [np.array([94, 80, 2]),   np.array([126, 255, 255]), (255, 0, 0)],
    "Red":   [np.array([0, 120, 70]),  np.array([10, 255, 255]), (0, 0, 255)],
    "Orange": [np.array([11, 100, 100]), np.array([25, 255, 255]), (0, 165, 255)],
    #"White": [np.array([0, 0, 150]), np.array([180, 20, 255]), (255, 255, 255)],
    # You can add more here:
    # "Red": [np.array([0, 120, 70]), np.array([10, 255, 255]), (0, 0, 255)]
}
if __name__ == "__main__":
    while True:
        ret, frame = video.read()
        if not ret: break

        # Convert to HSV once per frame
        hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # 2. Loop through every color in our library
        for color_name, (lower, upper, draw_color) in color_library.items():
            # Create a mask for THIS specific color
            mask = cv2.inRange(hsv_frame, lower, upper)
            
            # Clean up the mask (remove speckles)
            mask = cv2.dilate(mask, None, iterations=1)

            # 3. Find the objects of this color
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > 800: # Only track objects larger than 800 pixels
                    x, y, w, h = cv2.boundingRect(cnt)
                    
                    # Draw the box and the name of the color found
                    cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
                    cv2.putText(frame, color_name, (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, draw_color, 2)
                    
                    #Find object centre
                    cx = x + w // 2
                    cy = y + h // 2
                    cv2.circle(frame, (cx, cy), 5, draw_color, -1)

                    #Print the coordinates of the object centre once per second
                    print(f"{color_name} object at: ({cx}, {cy})")

        # 4. Show the result
        cv2.imshow("Multi-Color Tracker", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

video.release()
cv2.destroyAllWindows()