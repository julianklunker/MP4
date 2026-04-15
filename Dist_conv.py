class LinearConverter:
    def __init__(self):
        self.scale = 0.0
        self.offset = 0.0

    def calibrate(self, pixel_x1, robot_x1, pixel_x2, robot_x2):
        # Calculate the slope (m)
        self.scale = (robot_x2 - robot_x1) / (pixel_x2 - pixel_x1)
        
        # Calculate the y-intercept (b)
        self.offset = robot_x1 - (self.scale * pixel_x1)
        print(f"Scale={self.scale:.4f} mm/pixel, Offset={self.offset:.2f} mm")

    def convert_x(self, pixel_x):
        robot_x = (self.scale * pixel_x) + self.offset
        return robot_x
    
    def y_timing(self, belt_speed):
        bot1_distance_mm = 530
        bot2_distance_mm = 1190
        bot1_time_s = bot1_distance_mm / belt_speed
        bot2_time_s = bot2_distance_mm / belt_speed
        return bot1_time_s, bot2_time_s


if __name__ == "__main__":
    converter = LinearConverter()
    
    converter.calibrate(pixel_x1=20, robot_x1=30.0, pixel_x2=1200, robot_x2=-30.0)
    
    detected_pixel = 350
    final_robot_x = converter.convert_x(detected_pixel)
    
    print(f"Cam Pixel {detected_pixel}")
    print(f"G0 X{final_robot_x:.2f}")