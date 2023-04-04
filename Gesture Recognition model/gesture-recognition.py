#!/usr/bin/env python3
import tensorflow as tf 
from keras.models import load_model
import cv2
import numpy as np
from random import choice

REV_CLASS_MAP = {
    0: "gesture1",
    1: "nothing",
}


def mapper(val):
    return REV_CLASS_MAP[val]

model = load_model("model.h5")

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))

prev_move = None

while True:
    ret, frame = cap.read()
    if not ret:
        continue

    cv2.rectangle(frame, (10, 70), (300, 340), (0, 255, 0), 2)
    #cv2.rectangle(frame, (330, 70), (630, 370), (255, 0, 0), 2)

    # extract the region of image within the user rectangle
    roi = frame[70:300]
    img = cv2.cvtColor(roi, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (227, 227))

    # predict the move made
    pred = model.predict(np.array([img]))
    gesture_code = np.argmax(pred[0])
    gesture_name = mapper(gesture_code)

    # predict the winner (human vs computer)
   # if prev_move != gesture_name:
        #if gesture_name == "nothing":
            #gesture = "Waiting..."
    #prev_move = gesture_name

    # display the information
    font = cv2.FONT_HERSHEY_SIMPLEX
    #cv2.putText(frame, "Your Move: " + gesture_name,
                #(10, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    #cv2.putText(frame, "Pi's Move: " + computer_move_name,
                #(330, 50), font, 1, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Gesture: " + gesture_name,
                (100, 450), font, 2, (0, 255, 0), 4, cv2.LINE_AA)

    #if computer_move_name != "nothing":
        #icon = cv2.imread(
            #"test_img/{}.png".format(computer_move_name))
        #icon = cv2.resize(icon, (300, 300))
        #frame[70:370, 330:630] = icon

    #cv2.imshow("Rock Paper Scissors", frame)

    k = cv2.waitKey(10)
    if k == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
