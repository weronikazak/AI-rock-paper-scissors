import cv2
import numpy as np
import os
from random import shuffle
from shutil import copyfile
IMAGES = os.listdir(os.getcwd() + "/images")
IMAGES = set([i.split(".")[0] for i in IMAGES])
IMAGES = list(IMAGES)
shuffle(IMAGES)


SPLIT = int(0.8 * len(IMAGES))
train = IMAGES[:SPLIT]
test = IMAGES[SPLIT:]
img_id = 1

for img in train:
	new_path = os.getcwd() + "\\imgs\\train\\" + "img_" + str(img_id)
	org_path = os.getcwd() + "\\images\\" + img 
	img_id += 1
	exts = [".jpg", ".xml"]
	for e in exts:
		copyfile(org_path + e, new_path + e)

for img in test:
	new_path = os.getcwd() + "\\imgs\\test\\" + "img_" + str(img_id)
	org_path = os.getcwd() + "\\images\\" + img
	img_id += 1
	exts = [".jpg", ".xml"]
	for e in exts:
		copyfile(org_path + e, new_path + e)