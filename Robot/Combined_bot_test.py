import serial
import time
#import sys
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
        
    def get_pos(self):
        super().reset_input_buffer()
        self.write("G93")
        response = super().read(16)
        print(type(response))
        #pos = response[2:-1].split(",")
        #print(pos)
    
    def read_serial(self):
        msg = self.read(16)
        return msg
        
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


class Sorting_bot(Maxi):
    def __init__(self, port, *args, **kwargs):
        try :
            super().__init__(port, *args, **kwargs)
        except:
            print("Error")
        
        if not self:
            print("Not working")
        
        self.Z_PICKUP = 0
        self.Z_BEFORE_PUMP = 30
        self.Z_FOR_MOVE = 150
        self.Z_FOR_DROPOFF = 30
        self.drop_locs = {"red": (150,0),
                          "item1": (150,150),
                          "item2": (150,-150),
                          "item3": (-150,0),
                          "item4": (-150,150),
                          "item5": (-150,-150)}
        
        self.queue = []
        self.item = False
        self.time_next = 0
        self.picktime = 2
        self.droptime = 2
        self.working = False
      

    def pickup(self,pos):
        print(self.item)
        self.time_next = time.time()+self.picktime
        self.working = True
        selv.move(z=self.Z_FOR_MOVE)
        self.move(x=pos)
        self.move(z=self.Z_BEFORE_PUMP)
        self.pump_on()
        self.move(z=self.Z_PICKUP)
        self.move(z=self.Z_FOR_MOVE)
    
    def dropoff(self,item):
        print(self.item)
        self.time_next = time.time()+self.droptime
        self.working = False
        X_DROP, Y_DROP = self.drop_locs[item]
        self.move(x=X_DROP, y=Y_DROP)
        self.move(z=self.Z_FOR_DROPOFF)
        self.move(x=0,y=0,z=self.Z_FOR_MOVE)
     
    def read_queue(self):
        try:
            self.item = self.queue.pop(0)
        except: 
            self.item = False

    def status(self):
        if time.time() >= self.time_next:
            if self.working:
                print("Dropping")
                self.dropoff(self.item[0])
                self.item = False
            else:
                self.read_queue()
                if self.item:
                    print("Picking")
                    self.pickup(self.item[1])
            return True
        else:
            return False

    def get_response(self):
        msg = self.read(8)
        self.reset_input_buffer()
        print(msg)
        if msg:
            return True
        else:
            return False
 
        
class Sorting_bot_mini(MiniMHbot):
    def __init__(self, port, *args, **kwargs):
        #try :
        super().__init__(port, *args, **kwargs)
        #except:
        #    print("Error")
        
        if not self:
            print("Not working")
        
        self.Z_PICKUP = 50
        self.Z_BEFORE_PUMP = 70
        self.Z_FOR_MOVE = 150
        self.Z_FOR_DROPOFF = 40
        self.drop_locs = {"item0": (-100,0),
                          "item1": (10,10),
                          "item2": (10,-10),
                          "item3": (-10,0),
                          "item4": (-10,10),
                          "item5": (-10,-10)}

        self.queue = []
        self.item = 0
        self.time_next = 0
        self.picktime = 50
        self.droptime = 50
        self.working = False
        
    def pickup(self,pos):
        self.time_next = time.time()+self.picktime
        self.move(x=pos)
        self.move(z=self.Z_BEFORE_PUMP)
        #self.pump_on()
        self.move(z=self.Z_PICKUP)
        self.move(z=self.Z_FOR_MOVE)
    
    def dropoff(self,item):
        self.time_next = time.time()+self.droptime
        X_DROP, Y_DROP = self.drop_locs[item]
        self.move(x=X_DROP, y=Y_DROP)
        self.move(z=self.Z_FOR_DROPOFF)
        #self.pump_off()
        self.move(z=self.Z_FOR_MOVE)
    
    def read_queue(self):
        try:
            self.item = self.queue.pop(0)
        except: 
            self.item = False

    def status(self):
        if time.time() >= self.time_next:
            if working:
                self.dropoff(self.item[0])
            else:
                self.read_queue()
                if self.item:
                    self.pickup(self.item[1])
            return True
        else:
            return False
    
    def get_response(self):
        msg = self.read(8)
        self.reset_input_buffer()
        print(msg)
        if msg:
            return True
        else:
            return False
    
    """
    def pickup(self,pos):
        self.move(x=pos)
        self.get_response()
        self.move(z=self.Z_BEFORE_PUMP)
        self.get_response()
        #self.pump_on()
        #self.get_response()
        self.move(z=self.Z_PICKUP)
        self.get_response()
        self.move(z=self.Z_FOR_MOVE)
        self.get_response()
    
    def dropoff(self,item):
        X_DROP, Y_DROP = self.drop_locs[item]
        self.move(x=X_DROP, y=Y_DROP)
        self.get_response()
        self.move(z=self.Z_FOR_DROPOFF)
        #self.get_response()
        #self.pump_off()
        self.get_response()
        self.move(z=self.Z_FOR_MOVE)
        self.get_response()
        
    def get_response(self):
        while True:
            print("Reading")
            msg = self.read(8)
            self.reset_input_buffer()
            print(msg)
            if msg:
                break
        return True
    """
    
    
"""
def initBot(args):
    print("type: ", args[1])
    print("COM port: ", args[2])

if __name__ == "__main__":
    initBot(sys.argv)
"""
