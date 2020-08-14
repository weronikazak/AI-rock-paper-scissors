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
user_points, comp_points = 0, 0

verdict = "VERDICT"


def create_hand_frame(frame):
    new_frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    r, new_frame = cv2.threshold(new_frame, 30, 255, cv2.THRESH_BINARY_INV)
    return new_frame


def prepare_frame(frame):
    new_frame = cv2.resize(frame, (IMG_SIZE, IMG_SIZE))
    return new_frame.reshape(-1, IMG_SIZE, IMG_SIZE, 1)


def display_predicition(frame):
    new_frame = prepare_frame(frame)
    prediction = model.predict(new_frame)
    return SIGNS[np.argmax(prediction)]


def compare_signs(user_sign, comp_sign, GAME_ON, user_points, comp_points, verdict):
    if user_sign == "quit":
        verdict = "YOU QUITED"
        GAME_ON = False
    elif user_sign == "none":
        comp_points += 1
        verdict = "POINT FOR PC!"
    elif user_sign == comp_sign:
        verdict = "REMIS!"
    else:
        if user_sign == "scissors":
            if comp_sign == "rock":
                verdict = "POINT FOR PC!"
                comp_points += 1
            else:
                verdict = "POINT FOR YOU!"
                user_points += 1
        elif user_sign == "rock":
            if comp_sign == "paper":
                verdict = "POINT FOR PC!"
                comp_points += 1
            else:
                verdict = "POINT FOR YOU!"
                user_points += 1
        elif user_sign == "paper":
            if comp_sign == "scissors":
                verdict = "POINT FOR PC!"
                comp_points += 1
            else:
                verdict = "POINT FOR YOU!"
                user_points += 1
    return GAME_ON, user_points, comp_points, verdict

count_frames = 1
countdown = 200
secs = 0

while GAME_ON == True:

    while count_frames <= countdown*1.5 + 1:
        ret, frame = camera.read()

        cv2.flip(frame, 1,frame)

        hand_frame = frame[top:bottom, left:right]
        hand_frame = create_hand_frame(hand_frame)

        sign = display_predicition(hand_frame)

        cv2.putText(frame, sign, (50, 50), font, 1, (0, 255, 255), 2)

        cv2.putText(frame, str(user_points), (400, 50), font, 1, (0, 255 , 255), 2)
        cv2.putText(frame, str(comp_points), (450, 50), font, 1, (255, 0, 0), 2)

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)

        # DISPLAY COUNTDOWN TO 3 BEFORE SHOWING SIGN
        if count_frames <= countdown:
            secs = count_frames
        cv2.putText(frame, str(int((secs+2)/50)), (50, 400), font, 2, (255, 255, 255), 3)

        if count_frames >= countdown:
            if count_frames == countdown:
                comp_sign = random.choice(SIGNS[:-2])
                GAME_ON, user_points, comp_points, verdict = compare_signs(sign, comp_sign, GAME_ON, user_points, comp_points, verdict)


            cv2.putText(frame, verdict, (100, 200), font, 2, (0, 0, 255), 4)
            cv2.putText(frame, comp_sign, (200, 50), font, 1, (255, 0, 0), 2)

        if GAME_ON == False: break

        cv2.imshow("frame", frame)
        cv2.imshow("hand", hand_frame)

        count_frames += 1

        if cv2.waitKey(20) & 0xFF == ord('q'):
            GAME_ON = False
            break
        

    count_frames = 1


camera.release()
cv2.destroyAllWindows()