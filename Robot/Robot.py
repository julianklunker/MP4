import serial
from time import time, sleep

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
        super().__init__(port, baudrate=115200, timeout=10, *args)
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
        print(response)
        # print(type(response))
        #pos = response[2:-1].split(",")
        #print(pos)

    def close_con(self):
        super().close()
        if self.is_open:
            print("Could not disconnect")
        else:
            print("Closed the connection")

class Sorting_bot(Robot):
    def __init__(self, port, *args, **kwargs):
        super().__init__(port, *args, **kwargs)

        self.queue = []
        self.item = False
        self.time_next = 0
        self.working = False

    def pickup(self,pos,item_time):
        # print(self.item)
        self.time_next = time()+self.picktime
        self.working = True
        self.move(z=self.Z_FOR_MOVE)
        Y_PICKUP = (time() - item_time) * self.belt_speed - self.Y
        print(Y_PICKUP)
        # print(self.belt_speed)
        self.move(x=pos,y=Y_PICKUP)
        self.move(z=self.Z_BEFORE_PUMP)
        self.pump_on()
        self.move(z=self.Z_PICKUP)
        self.move(z=self.Z_FOR_MOVE)

    def dropoff(self,item):
        # print(self.item)
        self.time_next = time()+self.droptime
        self.working = False
        X_DROP, Y_DROP = self.drop_locs[item]
        self.move(x=X_DROP, y=Y_DROP)
        self.move(z=self.Z_FOR_DROPOFF)
        self.pump_off()
        # self.move(x=0,y=0,z=self.Z_FOR_MOVE)
        self.move(z=self.Z_FOR_MOVE)

    def read_queue(self):
        try:
            loc = (time() - self.queue[0][2]) * self.belt_speed - self.Y
            if loc > self.Y_MIN:
                self.item = self.queue.pop(0)
            if loc > self.Y_MAX:
                self.missed_item += 1
                print("Missed an item")
                raise
        except:
            self.item = False

    def status(self):
        if time() >= self.time_next:
            if self.working:
                print("Dropping")
                self.dropoff(self.item[0])
                self.item = False
            else:
                self.read_queue()
                if self.item:
                    print("Picking")
                    self.pickup(self.item[1],self.item[2])
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

class Maxi(Sorting_bot):
    def __init__(self, port, *args, **kwargs):
        print("Init Maxi bot")
        super().__init__(port, *args, **kwargs)
        self.z_offset = -825

        self.Z_PICKUP = 50
        self.Z_BEFORE_PUMP = 80
        self.Z_FOR_MOVE = 150
        self.Z_FOR_DROPOFF = 80
        self.Y = 500
        self.Y_MIN = -200
        self.Y_MAX = 200
        self.picktime = 1
        self.droptime = 1
        self.belt_speed = 50. #mm/s
        # self.drop_locs = {"Red": (200,0),
        #                   "Green": (200,170),
        #                   "Blue": (200,-170),
        #                   "Yellow": (-200,0),
        #                   "Purple": (-200,170),
        #                   "Brown": (-200,-170)}
        self.drop_locs = {"Red": (180,30),
                          "Green": (180,30),
                          "Blue": (-130,25),
                          "Yellow": (-200,0),
                          "Purple": (-200,170),
                          "Brown": (-200,-170)}

        self.missed_items = 0

        def set_speed(self, speed: int):
            super().set_speed(speed)
            self.picktime = (2.*(2000-speed)+0.1*(speed-100))/(2000-100)
            self.droptime = self.picktime
            print(self.picktime)
