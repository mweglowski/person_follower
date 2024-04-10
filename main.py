from djitellopy import tello
import time
import cv2
import numpy as np

import keyboard_control
import image_processing
import detection


def initialize_drone():
    drone = tello.Tello()
    drone.connect()
    print(f"BATTERY -> {drone.get_battery()}")
    print(f"TEMPERATURE -> {drone.get_temperature()}")
    time.sleep(3)
    return drone

def main():
    keyboard_control.init()
    # drone = initialize_drone()
    # drone.streamon()
    
    cap = cv2.VideoCapture(0)

    while True:
        _, image = cap.read()
        # image = drone.get_frame_read().frame
        image = cv2.resize(image, (600, 400))

        image_numpy = np.array(image)
        # Visualization of person detection
        box_coords = detection.visualize_detections(image_numpy)
        print(box_coords)

        # Controlling drone
        # control_values = keyboard_control.control_input(drone)
        # drone.send_rc_control(control_values[0], control_values[1], control_values[2], control_values[3])
        time.sleep(0.05)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # drone.streamoff()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
