import cv2
import numpy as np

camera = cv2.VideoCapture(0)
img_id = 348
k = 1

while True:
	ret, frame = camera.read()

	if cv2.waitKey(1) == ord('c'):
		START = not START
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

	if k % 11 == 0:
		cv2.imwrite(f'images/image_{img_id}.jpg', frame)
		img_id += 1
	cv2.imshow('img', frame)
	k+= 1

camera.release()
cv2.destroyAllWindows()