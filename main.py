from djitellopy import tello
import key_press as kp
import time
import cv2
import numpy as np
import image_processing
import detection

def initialize_drone():
    drone = tello.Tello()
    drone.connect()
    print(f"BATTERY -> {drone.get_battery()}")
    print(f"TEMPERATURE -> {drone.get_temperature()}")
    time.sleep(3)
    return drone

def control_keyboard_input(drone):
    speed = 50
    lr, fb, ud, yw = 0, 0, 0, 0

    if kp.get_key("w"):
        fb = speed
    elif kp.get_key("s"):
        fb = -speed
    if kp.get_key("a"):
        lr = -speed
    elif kp.get_key("d"):
        lr = speed
    if kp.get_key("SPACE"):
        ud = speed
    elif kp.get_key("LCTRL"):
        ud = -speed
    if kp.get_key("RIGHT"):
        yw = speed
    elif kp.get_key("LEFT"):
        yw = -speed
    if kp.get_key("t"):
        drone.takeoff()
    if kp.get_key("q"):
        drone.land()
        time.sleep(4)
    return [lr, fb, ud, yw]

def main():
    kp.init()
    drone = initialize_drone()
    drone.streamon()
    
    # cap = cv2.VideoCapture(0)

    while True:
        image = drone.get_frame_read().frame
        # _, image = cap.read()
        image = cv2.resize(image, (480, 320))
        # cv2.imshow("Drone view", image)

        # np.array([...])
        image_numpy = np.array(image)
        # tf.Tensor([...])
        input_tensor = image_processing.convert_to_tensor(image_numpy)
        
        # Visualization of person detection
        detection.visualize_detections(image, input_tensor)

        # Controlling drone
        control_values = control_keyboard_input(drone)
        drone.send_rc_control(control_values[0], control_values[1], control_values[2], control_values[3])
        time.sleep(0.05)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    drone.streamoff()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
