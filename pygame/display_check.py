import cv2
import tensorflow as tf
import numpy as np
import random

camera = cv2.VideoCapture(0)
top, right, bottom, left = 150, 600, 400, 350

SIGNS = ["rock", "paper", "scissors", "quit", "none"]
IMG_SIZE = 50
model = tf.keras.models.load_model("RPS.model")

font = cv2.FONT_HERSHEY_SIMPLEX

GAME_ON = True


def create_hand_frame(frame):
    new_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    r, new_frame = cv2.threshold(new_frame, 30, 255, cv2.THRESH_BINARY)
    return new_frame


def prepare_frame(frame):
    new_frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    return new_frame.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


def display_predicition(frame):
    new_frame = prepare_frame(frame)
    prediction = model.predict(new_frame)
    return SIGNS[np.argmax(prediction)]


while GAME_ON == True:
    ret, frame = camera.read()

    cv2.flip(frame, 1,frame)

    hand_frame = frame[top:bottom, left:right]
    hand_frame = create_hand_frame(hand_frame)

    sign = display_predicition(hand_frame)

    cv2.putText(frame, sign, (50, 50), font, 1, (0, 255 , 255), 2)
    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

    cv2.imshow("frame", frame)
    cv2.imshow("hand", hand_frame)

    if cv2.waitKey(20) & 0xFF == ord('q'):
        break


camera.release()
cv2.destroyAllWindows()