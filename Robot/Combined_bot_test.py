import serial
import time
import sys
#import threading
#import re

#from sortingsystem.settings import config


class Robot(serial.Serial):
    """
    Base class for all robots.

    Inherits from Serial class.

    Attributes:
        z_offset (int): The offset value for the Z-axis position.

    Methods:
        write(gcode: str): Writes the specified G-code to the robot.
        set_speed(speed: int): Sets the speed of the robot.
        set_acceleration(acceleration: int): Sets the acceleration of the robot.
        home(): Moves the robot to the home position.
        move(**pos): Moves the robot to the specified position.
        pump_on(): Turns on the pump of the robot.
        pump_off(): Turns off the pump of the robot.
        pause(t: float): Pauses the robot for a specified duration.
    """

    def __init__(self, port, *args, **kwargs):
        """
        Initialize the Robot object.

        Args:
            port (str): The port to connect to the robot.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            z_offset (int): The z-axis offset value.

        """
        super().__init__(port, baudrate=115200, timeout=10, *args, **kwargs)
        self.z_offset = 0

    def write(self, gcode: str):
        """
        Writes the specified G-code to the robot.

        Args:
            gcode (str): The G-code to be written.
        """
        super().write(f"{gcode} \n".encode())

    def set_speed(self, speed: int):
        """
        Sets the speed of the robot.

        Args:
            speed (int): The speed value to be set.
        """
        self.move(F=speed)

    def set_acceleration(self, acceleration: int):
        """
        Sets the acceleration of the robot.

        Args:
            acceleration (int): The acceleration value to be set.
        """
        self.move(A=acceleration)

    def home(self):
        """
        Moves the robot to the home position.
        """
        self.write("G28")

    def move(self, **pos):
        """
        Moves the robot to the specified position.

        Args:
            **pos: Keyword arguments representing the position values.
        """
        gcode = "G01"
        for key, value in pos.items():
            key = key.upper()
            if key == "X":
                gcode += " X" + str(value)
            elif key == "Y":
                gcode += " Y" + str(value)
            elif key == "Z":
                gcode += " Z" + str(value + self.z_offset)
            elif key == "F":
                gcode += " F" + str(value)
            elif key == "A":
                gcode += " A" + str(value)
            elif key == "P":
                gcode = "G04 P" + str(value)
            elif key == "M":
                if len(str(value)) < 2:
                    gcode = "M" + "0" + str(value) + " D0"
                else:
                    gcode = "M" + str(value)
        self.write(gcode)

    def pump_on(self):
        """
        Turns on the pump of the robot.
        """
        self.write("M03 D0")

    def pump_off(self):
        """
        Turns off the pump of the robot.
        """
        self.write("M05 D0")

    def pause(self, t: float):
        """
        Pause the robot for a specified duration.

        Args:
            t (float): The duration of the pause in miliseconds.
        """
        self.write(f"G04 P{t}")
        
    def getPos(self):
        super().reset_input_buffer()
        self.write("G93")
        response = super().read(16)
        print(type(response))
        #pos = response[2:-1].split(",")
        #print(pos)
        
        
    def closeCon(self):
        super().close()
        if self.is_open:
            print("Could not disconnect")
        else:
            print("Closed the connection")


class MiniMHbot(Robot):
    """
    Class for Mini bot build by Mogens Hinge.
    """

    def __init__(self, port, *args, **kwargs):
        super().__init__(port, *args, **kwargs)

        self.z_offset = -383

    def write(self, gcode: str):
        super().write(gcode)
        time.sleep(0.01)
        
class Maxi(Robot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.z_offset = -825
        
def initBot(args):
    print("type: ", args[1])
    print("COM port: ", args[2])
"""
if __name__ == "__main__":
    initBot(sys.argv)
"""