# from:https://software.intel.com/en-us/articles/OpenVINO-Install-RaspberryPI
import cv2 as cv
import time
import sys
from adafruit_servokit import ServoKit
from pysabertooth import Sabertooth
from multiprocessing import Process, Queue, Manager

servo_kit = ServoKit(channels=16)
pan_servo = servo_kit.servo[0]
tilt_servo = servo_kit.servo[1]
pan_angle = 100
tilt_angle = 140

saber = Sabertooth('/dev/ttyS0')

cam_buffer = None
detection_buffer = None
out = None
center = None
area = None

net = cv.dnn.readNet('frozen_inference_graph.xml', 'frozen_inference_graph.bin')
# Specify target device
net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

label_font = cv.FONT_HERSHEY_SIMPLEX


def start_camera(cam_buffer, detection_buffer, center_buffer, area_buffer):
    global out
    global center
    global area

    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, 320)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, 240)
    time.sleep(3)
    while True:
        ret, frame = cap.read()

        # Prepare input blob and perform an inference
        if cam_buffer.empty():
            cam_buffer.put(frame)

        if not detection_buffer.empty():
            out = detection_buffer.get()

        if out is not None:
            # Draw detected faces on the frame
            for detection in out.reshape(-1, 7):
                confidence = float(detection[2])
                xmin = int(detection[3] * frame.shape[1])
                ymin = int(detection[4] * frame.shape[0])
                xy_min = (xmin, ymin)
                xmax = int(detection[5] * frame.shape[1])
                ymax = int(detection[6] * frame.shape[0])
                xy_max = (xmax, ymax)

                xmid = (xmax + xmin) // 2
                ymid = (ymax + ymin) // 2

                if confidence > 0.5:
                    x = xmax - xmin
                    y = ymax - ymin
                    area = x * y
                    area_buffer.put(area)
                    center = (xmid, ymid)
                    center_buffer.put(center)
                    detection_details = [xy_min, xy_max, center, confidence]
                    frame = image_overlay(frame, detection_details)

        #        if center is not None:
        #            move_servo_to_position(center[0], center[1])
        #            follow(area)

        if area is None:
            saber.stop()

        center = None
        area = None

        cv.imshow('frame', frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv.destroyAllWindows()


def image_overlay(image, details):
    overlay = image
    xy_min = details[0]
    xy_max = details[1]
    center = details[2]
    confidence = details[3]
    cv.rectangle(overlay, xy_min, xy_max, color=(0, 255, 0))
    cv.circle(overlay, center, 4, (255, 0, 0), 2)
    cv.putText(overlay, 'piggy: ' + str(round(confidence, 2) * 100) + '%', (xy_min[0] + 2, xy_min[1] + 10), label_font,
               0.3, (255, 255, 255), 1, cv.LINE_AA)
    return overlay


def start_detection(cam_buffer, detection_buffer):
    global net
    global out
    while True:
        if not cam_buffer.empty():
            frame = cam_buffer.get()
            blob = cv.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv.CV_8U)
            net.setInput(blob)
            out = net.forward()
            detection_buffer.put(out)


def move_servo_to_position(center_buffer, pan, tilt):
    global pan_servo
    global tilt_servo
    global pan_angle
    global tilt_angle

    angle_increment = 2.5

    while True:

        if center_buffer.empty():
            continue

        center = center_buffer.get()
        x, y = center[0], center[1]

        if x < 120:
            pan_angle -= angle_increment
            if pan_angle < 10:
                pan_angle = 10
            pan_servo.angle = pan_angle
            pan.value = pan_angle
        if x > 200:
            pan_angle += angle_increment
            if pan_angle > 170:
                pan_angle = 170
            pan_servo.angle = pan_angle
            pan.value = pan_angle
        if y < 80:
            tilt_angle += angle_increment
            if tilt_angle > 170:
                tilt_angle = 170
            tilt_servo.angle = tilt_angle
            tilt.value = tilt_angle
        if y > 160:
            tilt_angle -= angle_increment
            if tilt_angle < 10:
                tilt_angle = 10
            tilt_servo.angle = tilt_angle
            tilt.value = tilt_angle


def follow(area_buffer, pan):
    while True:
        #        time.sleep(0.2)
        if area_buffer.empty():
            continue

        area = area_buffer.get()
        pan_angle = pan.value

        follow_error = 100 - pan_angle
        forward_speed = constrain(100 - (area // 256), -25, 100)
        differential = (follow_error + (follow_error * forward_speed)) / 64

        left_speed = constrain(forward_speed - differential, -100, 100)
        right_speed = constrain(forward_speed + differential, -100, 100)
        print("area: {} follow_error: {} forward speed: {} differential: {} left_speed: {} right_speed: {}".format(area,
                                                                                                                   follow_error,
                                                                                                                   forward_speed,
                                                                                                                   differential,
                                                                                                                   left_speed,
                                                                                                                   right_speed))

        saber.drive(1, left_speed)
        saber.drive(2, right_speed)


def constrain(val, min_val, max_val):
    return min(max_val, max(min_val, val))


def main():
    global cam_buffer
    global detection_buffer

    processes = []

    pan_servo.angle = pan_angle
    tilt_servo.angle = tilt_angle
    saber.stop()

    try:
        with Manager() as manager:
            cam_buffer = Queue(maxsize=1)
            detection_buffer = Queue(maxsize=1)
            area_buffer = Queue(maxsize=1)
            center_buffer = Queue(maxsize=1)

            pan = manager.Value("i", 100)
            tilt = manager.Value("i", 140)

            camera_process = Process(target=start_camera,
                                     args=(cam_buffer, detection_buffer, center_buffer, area_buffer), daemon=True)
            camera_process.start()
            processes.append(camera_process)

            detection_process = Process(target=start_detection, args=(cam_buffer, detection_buffer), daemon=True)
            detection_process.start()
            processes.append(detection_process)

            pan_tilt_process = Process(target=move_servo_to_position, args=(center_buffer, pan, tilt), daemon=True)
            pan_tilt_process.start()
            processes.append(pan_tilt_process)

            follow_process = Process(target=follow, args=(area_buffer, pan), daemon=True)
            follow_process.start()
            processes.append(follow_process)

            for process in processes:
                process.join()

    except:
        import traceback
        traceback.print_exc()
    finally:
        saber.stop()
        for p in range(len(processes)):
            processes[p].terminate()

        sys.exit(0)


if __name__ == '__main__':
    main()
