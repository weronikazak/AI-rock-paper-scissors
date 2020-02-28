import cv2
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import numpy as np

model = tf.keras.models.load_model("RPS.model")

SIGNS = ["rock", "paper", "scissors", "quit", "none"]
IMG_SIZE = 50

def prepare_img(img):
    cv2.resize(img, (IMG_SIZE, IMG_SIZE), img)
    cv2.threshold(img, 127, 255, cv2.THRESH_BINARY, img)
    return np.reshape(-1, IMG_SIZE, IMG_SIZE, 1)

img_array = []

DIR = os.getcwd() + "\\imgs\\test"
for img in os.listdir(DIR):
    n_img = cv2.imread(os.path.join(DIR, img), 0)
    img_array.append(prepare_img(n_img))


f, arr = plt.subplots(3, 1)
arr[0, 0].imshow(img_array[0])
arr[0, 0].imshow(img_array[1])
arr[0, 0].imshow(img_array[2])
plt.show()
