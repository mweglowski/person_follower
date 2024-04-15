from djitellopy import tello
import time
import cv2
import numpy as np

import keyboard_control
import detection


def initialize_drone():
    drone = tello.Tello()
    drone.connect()
    print(f"BATTERY -> {drone.get_battery()}")
    print(f"TEMPERATURE -> {drone.get_temperature()}")
    time.sleep(3)
    return drone

def get_drone_controls(box_coords, image_size):
    forward_speed = 40
    angular_speed = 50
    
    x_min, y_min, x_max, y_max = box_coords
            
    box_width = abs(x_max - x_min)
    box_height = abs(y_max - y_min)
    box_area = box_height * box_width
    
    x_center = (x_max + x_min) // 2
    y_center = (y_max + y_min) // 2
    box_center = (x_center, y_center)
    
    image_width = image_size[0]
    image_height = image_size[1]
    image_area = image_width * image_height
    
    # Manipulating forward speed
    z_range = (0.2 * image_area, 0.3 * image_area)
    if box_area > z_range[0] and box_area < z_range[1]:
        fb = 0
    if box_area > z_range[1]:
        print("go back")
        fb = -forward_speed
    elif box_area < z_range[0]:
        print("go closer")
        fb = forward_speed
    
    # Manipulating horizontal speed
    x_range = (0.4 * image_width, 0.6 * image_width)
    if box_center[0] > x_range[0] and box_center[1] < x_range[1]:
        yw = 0
    if box_center[0] > x_range[1]:
        print(box_center, "turn camera right")
        yw = angular_speed
    elif box_center[0] < x_range[0]:
        print(box_center, "turn camera left")
        yw = -angular_speed
        
    # Manipulating vertical speed
    # y_range = (0.4 * image_height, 0.6 * image_height)
    # if box_center[1] > y_range[0] and box_center[1] < y_range[1]:
    #     ud = 0
    # if box_center[1] > y_range[1]:
    #     print("turn camera down")
    #     ud = -20
    # elif box_center[1] < y_range[0]:
    #     print("turn camera up")
    #     ud = 20
        
    # return (fb, 0, ud, yw)
    return (fb, 0, 0, yw)

def main():
    keyboard_control.init()
    drone = initialize_drone()
    drone.streamon()
    
    # cap = cv2.VideoCapture(0)
    drone.takeoff()
    
    image_size = (600, 400)

    while True:
        # _, image = cap.read()
        
        image = drone.get_frame_read().frame
        image = cv2.resize(image, image_size)

        image_numpy = np.array(image)
        
        # Visualization of person detection
        box_coords = detection.visualize_detections(image_numpy)
        
        if box_coords:
            fb, lr, ud, yw = get_drone_controls(box_coords, image_size)

            print(fb, lr, ud, yw)
            drone.send_rc_control(fb, lr, ud, yw)
            
        # Controlling drone
        control_values = keyboard_control.control_input(drone)
        drone.send_rc_control(control_values[0], control_values[1], control_values[2], control_values[3])
        time.sleep(0.05)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    drone.streamoff()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
