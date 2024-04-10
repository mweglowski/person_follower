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
    drone = initialize_drone()
    drone.streamon()

    while True:
        image = drone.get_frame_read().frame
        image = cv2.resize(image, (480, 320))

        # np.array([...])
        image_numpy = np.array(image)
        # tf.Tensor([...])
        input_tensor = image_processing.convert_to_tensor(image_numpy)
        
        # Visualization of person detection
        detection.visualize_detections(image, input_tensor)

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
