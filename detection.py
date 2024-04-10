import tensorflow as tf
import numpy as np
import cv2
import matplotlib.pyplot as plt

MODEL_PATH = './ssd_mobilenet_v2_320x320_coco17_tpu-8/saved_model'
model = tf.saved_model.load(MODEL_PATH)

def detect_object(image_numpy, model):
    input_tensor = tf.convert_to_tensor(image_numpy)
    detections = model(input_tensor)
    
    return detections

def draw_detections(image_numpy, detections, threshold=0.5):
    boxes = detections['detection_boxes'][0].numpy()
    classes = detections['detection_classes'][0].numpy().astype(np.int32)
    scores = detections['detection_scores'][0].numpy()

    # Filter detections by threshold and class 'person'
    indices = [i for i, (score, cls) in enumerate(zip(scores, classes)) if score > threshold and cls == 1]

    if indices:
        # Find the index of the highest confidence detection for 'person'
        best_idx = indices[np.argmax(scores[indices])]

        # Draw only the highest confidence bounding box
        box = boxes[best_idx] * np.array([image_numpy.shape[0], image_numpy.shape[1], image_numpy.shape[0], image_numpy.shape[1]])
        cv2.rectangle(image_numpy, (int(box[1]), int(box[0])), (int(box[3]), int(box[2])), (255, 0, 0), 2)

    return image_numpy

def visualize_detections(image, input_tensor):
    image_numpy = np.array(image)
    detections = detect_object(input_tensor, model)
    
    image_with_detections = draw_detections(image_numpy, detections)
    cv2.imshow("Detections", image_with_detections)
    cv2.waitKey(1)
