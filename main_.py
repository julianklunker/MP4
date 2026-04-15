from Camera.Camera import Camera
from Robot.Robot import Maxi
from Data_analysis.Tracker import Tracker
from time import sleep


def setup():
    Rob0 = Maxi("COM6")
    Rob1 = Maxi("COM3")
    Camera = False
    Tracker = False

    return (True, Rob0, Rob1, Camera, Tracker)

def main():
    print("Cam")
    sleep(5)
    print("Track")
    sleep(2)
    print("Pickup")
    sleep(2.5)
    print("Dropoff")
    print("Reset")
    sleep(4)
    return True

if __name__ == "__main__":
    running, Rob0, Rob1, Camera, Tracker = setup()
    print(running)

    while(running):
        running = main()
    print("\n---| END OF PROGRAM |---\n")
