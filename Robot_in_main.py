# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 10:37:02 2026

@author: Mancini
"""

from Robot.Combined_bot_test import Sorting_bot
import sys
import time


class Camera():
    
    def get_frame(self):
        return "Frame"

class Data_analysis():
    
    def analyze(self, frame):
        return (0,"item0")

if __name__ == "__main__":
    
    if sys.argv[1:]:
        com_port = "COM"+sys.argv[1]
    else:
        com_port = "COM" + input("Which COM port? (Just the number)\n")
    
    bot = Sorting_bot(com_port)
    print("start bot")
    bot.get_response()
    print("connected")
    #time.sleep(5)
    
    cam = Camera()
    data_analysis = Data_analysis()
    
    start_time = time.time()
    time_ = time.time()

    while True:
        if time.time()>start_time+2000:
            print("Stopping, too long")
            break
        print(time_)
        if time_ <= time.time() and len(bot.queue) < 10:
            print("Add to queue")
            bot.queue.append(["red",0,time.time()+1.5])
            time_ = time.time()+2
        print("Checking bot")
        print(len(bot.queue))
        bot.status()
        time.sleep(.5)
