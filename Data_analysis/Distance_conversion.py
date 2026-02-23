import numpy as np

#Fra venstre til højre er der 157 mm og 640 pixel



class Distance_conversion:
    def __init__ (self):
        self.conversion_rate = (503-95)/290
        self.robot_zero = 280

    def convert_x(self, x):
        robot_pickup_distance_pixel = float(x) - self.robot_zero
        robot_picup_distance_mm = robot_pickup_distance_pixel / self.conversion_rate
        return robot_picup_distance_mm