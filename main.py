import cv2
#import numpy as np
from time import time,sleep
from random import randint, choice, triangular
from sys import argv
from Camera.Camera import Camera
from Data_analysis.Tracker import Tracker
from Robot.Combined_bot_test import Maxi_bot, Mini_bot


items = ["Red","Green","Blue","Yellow","Purple","Brown","Rosso", "Verde", "Blau", "Giallo", "Viola","Marrone"]
items_mini = ["Ball","Disc","Brick"]

class _Camera():
    def __init__(self):
        self.img = cv2.imread("test_img.png", cv2.COLOR_BGR2HSV)
    def capture_frame(self):

        return self.img

class _Tracker():
    def object_information(self,img):
        item = choice(items)
        pos = randint(-100,100)
        return (item,pos,time())

if __name__ == "__main__":

    camera = Camera(camera_index=0)
    # print(dir(camera))
    camera.connect()
    tracker = Tracker()
    try:
        frame = camera.capture_frame()
        if frame == None:
            raise
    except:
        print("Could Not Connect, Using Mock")
        camera = _Camera()
        tracker =  _Tracker()
    # com_port = ""

    robs = []
    if argv[1:]:
        if argv[1].lower() == "mini":
            robot = Mini_bot(False)
            items = items_mini
            sleep(10)
            
    else:
        robot0 = Maxi_bot(False,n_bot=0)
        robot0.set_speed(500)
        robs.append(robot0)
        # robot1 = Maxi_bot(False,n_bot=1)
        # robot1.set_speed(500)
        # robs.append(robot1)

    new_item = time()

    for rob in robs:
        rob.move(x=0,y=0,z=100)

    item_test = [("Red",0,time()),("Green",0,time()),("Blue",0,time())]
    while True:

        frame = camera.capture_frame()

        # object_information = tracker.object_information(frame)
        if len(item_test) > 0:
            object_information = item_test.pop()
        cv2.imshow("Camera Feed", frame)

        if frame is not None:
            if object_information:
                #print(f"{object_information}")
                pass
        if cv2.waitKey(30) & 0xFF == ord('q'):
            for rob in robs:
                print(f"The robot missed:\n\t{rob.missed_items} items")
                rob.closeCon()
            break

        if len(robot0.queue) < 20 and time() > new_item:
            new_item = time()+triangular(0.05, 1.0, 0.1)
            print(f"{object_information}")
            if object_information[0] in items[:6]:
                robot0.queue.append(object_information)
            # else:
                # trans_item = items[items.index(object_information[0])-6]
                # print(object_information[0],trans_item)
                # object_information = (trans_item, object_information[1],object_information[2])
                # robot1.queue.append(object_information)

        # if len(robot1.queue) < 20 and time() > new_item:
        #     new_item = time()+triangular(0.05, 1.5, 0.1)
        #     print(f"{object_information}")
        #     robot1.queue.append(object_information)

        for rob in robs:
            rob.status()
