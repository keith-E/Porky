from adafruit_servokit import ServoKit
from pysabertooth import Sabertooth


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


class Servos:
    def __init__(self, start_pan_angle, start_tilt_angle):
        self.servo_kit = ServoKit(channels=16)
        self.pan_servo = self.servo_kit.servo[0]
        self.tilt_servo = self.servo_kit.servo[1]
        self.pan_angle = start_pan_angle
        self.tilt_angle = start_tilt_angle

        self.pan_servo.angle = self.pan_angle
        self.tilt_servo.angle = self.tilt_angle

    '''This method uses a primitive algorithm to point the camera at a an object within the frame.
            center_buffer: a multiprocessing queue that holds the center point of an object within a camera frame
            
            pan: a multiprocessing integer value that holds the location of the Pan Servo's angle
            tilt: a multiprocessing integer value that holds the location of the Tilt Servo's angle'''
    def follow(self, center_buffer, pan, tilt):
        # Adjust this variable to find the sweet spot for updating the pan and tilt values to follow an object with the
        # servos. Beware that setting this value too high may result in a rebound/bouncing effect.
        angle_increment = 2.5

        while True:

            if center_buffer.empty():
                continue

            center = center_buffer.get()
            x, y = center[0], center[1]

            if x < 120:
                self.pan_angle -= angle_increment
                if self.pan_angle < 10:
                    self.pan_angle = 10
                self.pan_servo.angle = self.pan_angle
                pan.value = self.pan_angle
            if x > 200:
                self.pan_angle += angle_increment
                if self.pan_angle > 170:
                    self.pan_angle = 170
                self.pan_servo.angle = self.pan_angle
                pan.value = self.pan_angle
            if y < 80:
                self.tilt_angle += angle_increment
                if self.tilt_angle > 170:
                    self.tilt_angle = 170
                self.tilt_servo.angle = self.tilt_angle
                tilt.value = self.tilt_angle
            if y > 160:
                self.tilt_angle -= angle_increment
                if self.tilt_angle < 10:
                    self.tilt_angle = 10
                self.tilt_servo.angle = self.tilt_angle
                tilt.value = self.tilt_angle


class Motors:
    def __init__(self):
        self.saber = Sabertooth('/dev/ttyS0')
        # Stop the motors just in case a previous run as resulted in an infinite loop.
        self.saber.stop()

    '''This method moves the base of the rover by controlling the left and right motors via the Sabertooth
       motor controller. 
       
                  area_buffer: a multiprocessing queue that contains areas of a given detected object
                  pan: a multiprocessing integer value for the pan angle managed by the multiprocessing manager'''
    def follow(self, area_buffer, pan):
        # Change this variable to increase the reverse speed while following, lower is faster (min = -100)
        saber_rmin_speed = -50
        # Change this variable to reduce the max forward speed, lower is slower (0 = stop)
        saber_fmax_speed = 100

        # Change this variable for more or less aggression while turning (the lower the value, the more aggressive the
        # turns). This should be determined while tuning to your environment. Weight of the rover, floor type, and wheel
        # traction are the some of the determining factors.
        turn_aggression = 64

        # Change this variable to adjust speed from the area given, if you're attempting to follow bigger objects in the
        # frame, set the value higher.
        proportional_area = 200

        while True:
            # If the area buffer is empty, skip over the code and start at the beginning to check again.
            if area_buffer.empty():
                self.saber.stop()
                continue

            area = area_buffer.get()
            pan_angle = pan.value
            # Determine how far off the center location (typically, the angle at which the Pan Servo points directly
            # forward). In this case, the Pan Servo starts at angle 100 degrees.
            follow_error = 100 - pan_angle

            # The forward speed is determined by the area of the object passed in via the area_buffer. This equation
            # results in faster speeds as the area gets smaller and slower speeds as the area gets bigger (eventually
            # reversing if the area is too large).
            forward_speed = constrain(100 - (area // proportional_area), saber_rmin_speed, saber_fmax_speed)

            # This equations sets the speed differential based on how far the object/pan angle is from the original
            # center location.
            differential = (follow_error + (follow_error * forward_speed)) / turn_aggression

            left_speed = constrain(forward_speed - differential, saber_rmin_speed, saber_fmax_speed)
            right_speed = constrain(forward_speed + differential, saber_rmin_speed, saber_fmax_speed)

            print("area: {} follow_error: {} forward speed: {} differential: {} left_speed: {} right_speed: {}"
                  .format(area,
                          follow_error,
                          forward_speed,
                          differential,
                          left_speed,
                          right_speed))

            self.saber.drive(1, left_speed)
            self.saber.drive(2, right_speed)
