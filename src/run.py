import sys
import argparse
from multiprocessing import Process, Queue, Manager
# Third-party libraries
from pysabertooth import Sabertooth
# Project modules
from camera import Camera
from motion import Servos, Motors
from detection import Detect


def main(cam_state, pt_state, mot_state):
    processes = []
  
    # Pan and Tilt Servo angles are determined by the HS-422 Servos and Adafruit ServoKit library used for this project.
    start_pan_angle = 100
    start_tilt_angle = 140

    try:
        with Manager() as manager:
            # Initialize the multiprocessing queue buffers. Setting a maxsize of 1 for the detection, area, and center buffers
            # currently results in optimal performance as there is some latency due to the Raspberry Pi environment.
            cam_buffer = Queue(10)
            detection_buffer = Queue(maxsize=1)
            area_buffer = Queue(maxsize=1)
            center_buffer = Queue(maxsize=1)
            
            # Initialize the multiprocessing manager values for the pan and tilt process to provide input to the pan/tilt and motor
            # processes.
            pan = manager.Value("i", start_pan_angle)
            tilt = manager.Value("i", start_tilt_angle)
            
            if cam_state == 1:
                cam = Camera()
                det = Detect(myriad=True)
                
                camera_process = Process(target=cam.start,
                                         args=(cam_buffer, detection_buffer, center_buffer, area_buffer), daemon=True)
                camera_process.start()
                processes.append(camera_process)

                detection_process = Process(target=det.start, args=(cam_buffer, detection_buffer), daemon=True)
                detection_process.start()
                processes.append(detection_process)
            
            if pt_state == 1:
                servo = Servos(start_pan_angle, start_tilt_angle)
                
                pan_tilt_process = Process(target=servo.follow, args=(center_buffer, pan, tilt), daemon=True)
                pan_tilt_process.start()
                processes.append(pan_tilt_process)
            
            if mot_state == 1:
                mot = Motors()
                
                motor_process = Process(target=mot.follow, args=(area_buffer, pan), daemon=True)
                motor_process.start()
                processes.append(motor_process)

            for process in processes:
                process.join()

    except:
        print("Unexpected error: ", sys.exc_info()[0])
        
    finally:
        for p in range(len(processes)):
            processes[p].terminate()

        # Ensure the motors are stopped before exiting.
        saber = Sabertooth('/dev/ttyS0')
        saber.stop()

        sys.exit(0)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Porky - The Real-Time Object Detection Robot')
    
    parser.add_argument('-cm', '--camerastate', dest='camera_state', type=int, default=1, 
                        help='Camera state: enabled or disabled. (0 - Disabled, 1 - Enabled, Default - 1)')
    parser.add_argument('pt', '--pantiltstate', dest='pan_tilt_state', type=int, default=1, 
                        help='Pan and Tilt state: enabled or disabled. (0 - Disabled, 1 - Enabled, Default - 1)')
    parser.add_argument('-mt', '--motorstate', dest='motor_state', type=int, default=1,
                        help='Motor state: enabled or disabled. (0 - Disabled, 1 - Enabled, Default - 1)')
    
    args = parser.parse_args()
    
    camera_state = args.camera_state
    pan_tilt_state = args.pan_tilt_state
    motor_state = args.motor_state
    
    main(camera_state, pan_tilt_state, motor_state)
