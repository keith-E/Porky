# from:https://software.intel.com/en-us/articles/OpenVINO-Install-RaspberryPI
import cv2 as cv
import time
import sys
from multiprocessing import Process, Queue, Manager

pan_angle = 100
tilt_angle = 140

cam_buffer = None
detection_buffer = None
out = None
center = None
area = None


def main():
    global cam_buffer
    global detection_buffer

    processes = []

    pan_servo.angle = pan_angle
    tilt_servo.angle = tilt_angle
    saber.stop()

    try:
        with Manager() as manager:
            cam_buffer = Queue(10)
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
