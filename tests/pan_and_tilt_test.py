import time
from adafruit_servokit import ServoKit

servo_kit = ServoKit(channels=16)
pan_servo = servo_kit.servo[0]
tilt_servo = servo_kit.servo[1]

pan_servo.angle = 100
tilt_servo.angle = 100

print('Executing pan and tilt test starting from 10 degrees and running until 170 degrees...')
for x in range(10, 171):
    pan_servo.angle = x
    tilt_servo.angle = x
    print('Servos are at: {} degrees'.format(x))
    time.sleep(0.2)