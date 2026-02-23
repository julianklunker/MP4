import cv2
import numpy as np
from Camera.Camera import Camera
from Data_analysis.Tracker import Tracker
from Robot.Combined_bot_test import Sorting_bot
from Data_analysis.Distance_conversion import Distance_conversion
import time

#initialize everything
camera = Camera(camera_index=1)
camera.connect()
bot = Sorting_bot("COM8")
print("start bot")
bot.get_response()
print("connected")
print("Going to zero")
bot.move(x=0,y=0,z=bot.Z_FOR_MOVE)
converter = Distance_conversion()
tracker = Tracker()

time.sleep(2)
print("Starting")
loc = 0
color = "None"

if __name__ == "__main__":
    while True:
        frame = camera.capture_frame()
        
        object_information = tracker.object_information(frame)

        cv2.imshow("Camera Feed", frame)

        if object_information is not None:

            color = object_information[0]
            loc = converter.convert_x(object_information[1])
            if len(bot.queue) < 10:
                bot.queue.append([color,loc,0])
        bot.status()
            #bot.get_response()
            
            #robot_working = True
            #while robot_working:
                #bot.get_response()
            
            
            
        if frame is not None:
            if object_information:
                print(f"{loc}")
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break