import sys

from multiprocessing import Process, Queue, Manager
from pysabertooth import Sabertooth

from .camera import Camera
from .motion import Servos, Motors
from .detection import Detect


def main():
    processes = []
    cam = Camera()
    det = Detect(myriad=True)
    start_pan_angle = 100
    start_tilt_angle = 140
    serv = Servos(start_pan_angle, start_tilt_angle)
    mot = Motors()

    try:
        with Manager() as manager:
            cam_buffer = Queue(10)
            detection_buffer = Queue(maxsize=1)
            area_buffer = Queue(maxsize=1)
            center_buffer = Queue(maxsize=1)

            pan = manager.Value("i", 100)
            tilt = manager.Value("i", 140)

            camera_process = Process(target=cam.start,
                                     args=(cam_buffer, detection_buffer, center_buffer, area_buffer), daemon=True)
            camera_process.start()
            processes.append(camera_process)

            detection_process = Process(target=det.start, args=(cam_buffer, detection_buffer), daemon=True)
            detection_process.start()
            processes.append(detection_process)

            pan_tilt_process = Process(target=serv.follow, args=(center_buffer, pan, tilt), daemon=True)
            pan_tilt_process.start()
            processes.append(pan_tilt_process)

            follow_process = Process(target=mot.follow, args=(area_buffer, pan), daemon=True)
            follow_process.start()
            processes.append(follow_process)

            for process in processes:
                process.join()

    except:
        import traceback
        traceback.print_exc()
    finally:
        for p in range(len(processes)):
            processes[p].terminate()

        # Ensure the motors are stopped.
        saber = Sabertooth('/dev/ttyS0')
        saber.stop()

        sys.exit(0)


if __name__ == '__main__':
    main()
