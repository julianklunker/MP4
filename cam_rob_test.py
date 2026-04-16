import cv2
import numpy as np
from time import time

from Camera import Camera
from robotclasses import Maxi
from Converter import Converter

# 1. Define our "Library" of colors (HSV ranges)
# Format: "ColorName": [Lower_Bound, Upper_Bound, Display_BGR_Color]
color_library = {
    "Green": [np.array([35, 100, 40]), np.array([85, 255, 255]), (0, 255, 0)],
    "Blue":  [np.array([94, 80, 40]),   np.array([126, 255, 255]), (255, 0, 0)],
    #"Red":   [np.array([0, 120, 70]),  np.array([10, 255, 255]), (0, 0, 255)],
    #"Orange": [np.array([11, 100, 100]), np.array([25, 255, 255]), (0, 165, 255)],
    #"White": [np.array([0, 0, 150]), np.array([180, 20, 255]), (255, 255, 255)],
    # You can add more here:
    # "Red": [np.array([0, 120, 70]), np.array([10, 255, 255]), (0, 0, 255)]
}

def setup():
    global cam
    global bot
    global converter

    cam = Camera()
    try:
        bot = Maxi("/dev/ttyACM0")
    except:
        print("Failed to connect to bot")
        bot = False
    if bot:
        bot.set_speed(750)
        bot.move(x=0,y=0)

    converter = Converter()
    converter.calibrate(0,90,cam.n_pixels,-90)


    #image = np.zeros((500, cam.n_pixels), dtype=np.uint8)
    global image
    image = np.zeros((cam.n_channels, cam.n_pixels,3), dtype=np.uint8)

    global objects
    objects = []

    global frame_time
    frame_time = time()

    global mode
    mode = 0

def update_image(image):
    line = cam.read_line()
    image = np.roll(image,1,axis=0)
    #image[0,:] =line.transpose()[:,500]
    height, width, _ = image.shape
    halv_width = int(width/2)
    #print(image.shape)
    image[0,:halv_width,0] =line.transpose()[:halv_width,500]
    image[0,halv_width:,1] =line.transpose()[halv_width:,500]
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    #rgb_image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    #hsv_image = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

    return (line, image, hsv_image)

def find_objects(image,hsv_image):
    # 2. Loop through every color in our library
    frame = image.copy()
    frame, objects = search_colors(frame, hsv_image)

    return frame, objects


def search_colors(frame, hsv_image):
    objects = []
    for color_name, (lower, upper, draw_color) in color_library.items():
        # Create a mask for THIS specific color
        mask = cv2.inRange(hsv_image, lower, upper)

        # Clean up the mask (remove speckles)
        mask = cv2.dilate(mask, None, iterations=1)

        # 3. Find the objects of this color

        frame, color_objects = find_contours(frame, mask, color_name, draw_color)
        if color_objects:
            objects += color_objects
    return frame, objects


def find_contours(frame, mask, color_name, draw_color):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    objects = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 800: # Only track objects larger than 800 pixels
            x, y, w, h = cv2.boundingRect(cnt)

            # Draw the box and the name of the color found
            cv2.rectangle(frame, (x, y), (x + w, y + h), draw_color, 2)
            cv2.putText(frame, color_name, (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX, 0.6, draw_color, 2)

            #Find object centre
            cx = x + w // 2
            cy = y + h // 2
            cv2.circle(frame, (cx, cy), 5, draw_color, -1)

            #Print the coordinates of the object centre once per second
            #print(f"{color_name} object at: ({cx}, {cy})")

            if y == 1:
                print(f"{color_name} object at: ({cx}, {cy})")
                objects.append((color_name,cx,time()))

    return frame, objects

def show(img,frame_time,mode):
    display = img.copy()
    fps = 1/(time()-frame_time)
    #print(f"fps: {fps}")
    frame_time = time()
    cv2.putText(display,f"fps: {int(fps)}", (0,30),cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.imshow("Multi-Color Tracker", display)
    k = cv2.waitKey(30) & 0xff
    if k == 27 or k == ord("q"):
        return (False, False, False)
    elif k == 32:
        mode += 1
        if mode > 2:
            mode = 0
    return (True, frame_time, mode)



def main(cam, image, bot, converter, objects, frame_time, mode):

    #For testing:
    num_on_box = 7.2
    belt_max_speed = 185
    belt_speed = num_on_box / 50 * belt_max_speed

    while True:

        #Get line from camera, roll image, add line to image, (image, hsv_image)
        line, image, hsv_image = update_image(image)

        frame, new_objects = find_objects(image, hsv_image)
        if new_objects:
            objects += new_objects
            print(f"Current objects:\n{objects}")

        # 4. Show the result
        options = [frame, image, line]
        more, frame_time, mode = show(options[mode],frame_time, mode)
        if not more:
            print(objects)
            break

        if bot.update():
            if objects and not bot.item:
                print(objects)
                item = objects.pop(0)
                bot_x = round(converter.convert_x(item[1]),2)
                time_at_bot = item[2] + converter.y_timing(belt_speed)[0]
                bot.item = (item[0], bot_x, time_at_bot)
                print(bot.item)
                bot.pickup()
            elif bot.item:
                bot.dropoff()


if __name__ == "__main__":
    setup()
    if bot:
        main(cam, image, bot, converter, objects, frame_time, mode)
    print("\n---| END OF PROGRAM |--\n")
