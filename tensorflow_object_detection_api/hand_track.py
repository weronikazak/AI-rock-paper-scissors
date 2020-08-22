import pathlib
import cv2
import io
import os
import scipy.misc
import numpy as np
import six
from six import BytesIO
import matplotlib
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFont
import tensorflow as tf
from object_detection.utils import visualization_utils as viz_utils

detect_fn = tf.saved_model.load('inference_graph/saved_model')
# image_dir = r'C:\Users\Weronika\Desktop\models-master\models\research\object_detection\hand_detection\images\test'

camera = cv2.VideoCapture(0)

# category_index = {
#     1: {'id': 1, 'name': 'rock'},
#     2: {'id': 2, 'name': 'paper'},
#     3: {'id': 3, 'name': 'scissors'},
#     4: {'id': 4, 'name': 'thumb'},
#     5: {'id': 5, 'name': 'other'}
# }

category_index = {
    1: {'id': 1, 'name': 'hand'},
    2: {'id': 2, 'name': 'hand'},
    3: {'id': 3, 'name': 'hand'},
    4: {'id': 4, 'name': 'hand'},
    5: {'id': 5, 'name': 'hand'}
}


def load_image_into_numpy_array(image):
  # img_data = tf.io.gfile.GFile(path, 'rb').read()
  # image = Image.open(BytesIO(img_data))
  (im_height, im_width) = image.shape[:2]
  return np.array(image).reshape(
      (im_height, im_width, 3)).astype(np.uint8)



while True:
    ret, frame = camera.read()
    frame_np = load_image_into_numpy_array(frame)
    input_tensor = np.expand_dims(frame_np, 0)
    detections = detect_fn(input_tensor)
    viz_utils.visualize_boxes_and_labels_on_image_array(
    	frame_np,
    	detections['detection_boxes'][0].numpy(),
    	detections['detection_classes'][0].numpy().astype(np.int32),
    	detections['detection_scores'][0].numpy(),
    	category_index,
    	use_normalized_coordinates=True,
    	max_boxes_to_draw=3,
    	min_score_thresh=.4,
    	agnostic_mode=False
    	)

    cv2.imshow('frame', frame_np)

    if cv2.waitKey(20) & 0xFF == ord("q"):
    	break

camera.release()
cv2.destroyAllWindows()