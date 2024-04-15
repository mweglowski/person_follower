import tensorflow as tf
import numpy as np
import cv2

MODEL_PATH = './ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
model = tf.saved_model.load(MODEL_PATH)

def detect_object(image_numpy, model):
    input_tensor = tf.convert_to_tensor(image_numpy, dtype=tf.uint8)
    input_tensor = tf.expand_dims(input_tensor, axis=0)  # Add batch dimension
    detections = model(input_tensor)
    return detections

def get_person_box_coordinates(image_numpy, detections, threshold=0.5):
    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int32)
    scores = detections['detection_scores'][0].numpy()

    indices = [i for i, (score, cls) in enumerate(zip(scores, classes)) if score > threshold and cls == 1]
    if indices:
        best_idx = indices[np.argmax(scores[indices])]
        best_box = boxes[best_idx]
        y_min, x_min, y_max, x_max = best_box
        y_min *= image_numpy.shape[0]
        y_max *= image_numpy.shape[0]
        x_min *= image_numpy.shape[1]
        x_max *= image_numpy.shape[1]
        return int(x_min), int(y_min), int(x_max), int(y_max)
    return None

def visualize_detections(image_numpy):
    detections = detect_object(image_numpy, model)
    box_coords = get_person_box_coordinates(image_numpy, detections)
    if box_coords:
        draw_detections(image_numpy, box_coords)
    cv2.imshow("Detections", image_numpy)
    cv2.waitKey(1)
    return box_coords

def draw_detections(image_numpy, box_coords):
    x_min, y_min, x_max, y_max = box_coords
    cv2.rectangle(image_numpy, (x_min, y_min), (x_max, y_max), (255, 0, 0), 2)
