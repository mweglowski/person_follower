import tensorflow as tf
import numpy as np

def convert_to_tensor(image_numpy):
	input_tensor = tf.convert_to_tensor(image_numpy)
	input_tensor = tf.expand_dims(input_tensor, 0)
	return input_tensor