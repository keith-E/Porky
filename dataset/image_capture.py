import RPi.GPIO as GPIO
import time
import numpy as np
import cv2 as cv

cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
cap.set(cv.CAP_PROP_FPS, 30.0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

piggy_prefix = "piggy-"
piggy_suffix = ".jpg"

# TODO: Make the image gathering dynamic -- aggregate the number of images within the directory to base the next number
image_count = 700

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        print("Can't receive frame. Exiting...")
        break
    cv.imshow('frame', frame)
    input_state = GPIO.input(18)
    piggy_filename = piggy_prefix + str(image_count) + piggy_suffix
    if input_state is False:
        print('Taking snapshot.')
        cv.imwrite(piggy_filename, frame)
        image_count = image_count + 1
        time.sleep(0.2)
        
    if cv.waitKey(1) & 0xFF == ord('q'):
        break
