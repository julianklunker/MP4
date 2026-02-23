import cv2

def check_cameras():
    for i in range(5):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) # CAP_DSHOW helps Windows open cameras faster
        if cap.isOpened():
            ret, frame = cap.read()
            if ret:
                print(f"Camera index {i} is AVAILABLE.")
            cap.release()
        else:
            print(f"Camera index {i} is NOT available.")

check_cameras()