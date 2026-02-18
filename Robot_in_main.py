# -*- coding: utf-8 -*-
"""
Created on Wed Feb 18 10:37:02 2026

@author: Mancini
"""

from Robot.Combined_bot_test import Sorting_bot
import sys

class Camera():
    
    def get_frame(self):
        return "Frame"

class data_analysis():
    
    def analyze(self):
        return (0,"item0")

if __name__ == "__main__":
    
    if sys.argv[1:]:
        com_port = "COM"+sys.argv[1]
    else:
        com_port = "COM" + input("Which COM port? (Just the number)\n")
    
    bot  = Sorting_bot(com_port)
    
    while True:
        frame = Camera.get_frame()
        pos, item_type = data_analysis.analyze(frame)
        bot.pickup(pos)
        bot.dropoff(item_type)


