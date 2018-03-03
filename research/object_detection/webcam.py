import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import mss

from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image


import cv2

sys.path.append("..")

from utils import label_map_util

from utils import visualization_utils as vis_util

MODEL_NAME = 'faster_inference_graph'

PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'

# List of the strings that is used to add correct label for each box.
PATH_TO_LABELS = os.path.join('data', 'object-detection.pbtxt')

NUM_CLASSES = 3

detection_graph = tf.Graph()
with detection_graph.as_default():
  od_graph_def = tf.GraphDef()
  with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
    serialized_graph = fid.read()
    od_graph_def.ParseFromString(serialized_graph)
    tf.import_graph_def(od_graph_def, name='')

label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
category_index = label_map_util.create_category_index(categories)

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)



with detection_graph.as_default():
  with tf.Session(graph=detection_graph) as sess:
    while True:
      # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
      monitor = {'top': 0, 'left': 0, 'width': 960, 'height': 540}
      pix = mss.mss().grab(monitor)
      image = Image.frombytes('RGB', pix.size, pix.rgb)
      #image = Image.open(imagename)
      image_np = load_image_into_numpy_array(image)
      
      image_np_expanded = np.expand_dims(image_np, axis=0)
      image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
      # Each box represents a part of the image where a particular object was detected.
      boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
      # Each score represent how level of confidence for each of the objects.
      # Score is shown on the result image, together with the class label.
      scores = detection_graph.get_tensor_by_name('detection_scores:0')
      classes = detection_graph.get_tensor_by_name('detection_classes:0')
      num_detections = detection_graph.get_tensor_by_name('num_detections:0')
      # Actual detection.
      (boxes, scores, classes, num_detections) = sess.run(
          [boxes, scores, classes, num_detections],
          feed_dict={image_tensor: image_np_expanded})
      width = 960
      height = 540
      ymin = boxes[0][0][0]*height
      xmin = boxes[0][0][1]*width
      ymax = boxes[0][0][2]*height
      xmax = boxes[0][0][3]*width
      print(ymin)
      print(xmin)
      print(ymax)
      print(xmax)     

      objects = []
      for index, value in enumerate(classes[0]):
          object_dict = {}
          if scores[0, index] > 0.5:
              object_dict[(category_index.get(value)).get('name').encode('utf8')] = \
                        scores[0, index]
              objects.append(object_dict)
      print(objects)

      # Visualization of the results of a detection.
      #vis_util.visualize_boxes_and_labels_on_image_array(
      #    image_np,
      #    np.squeeze(boxes),
      #    np.squeeze(classes).astype(np.int32),
      #    np.squeeze(scores),
      #    category_index,
      #    use_normalized_coordinates=True,
      #    line_thickness=8)

     # cv2.imshow('object detection', cv2.resize(image_np, (400,300)))
     # if cv2.waitKey(25) & 0xFF == ord('q'):
     #   cv2.destroyAllWindows()
     #   break
