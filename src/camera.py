import cv2 as cv
from detection import Classify


class Camera:
    def __init__(self, cam_width=320, cam_height=240):
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cam_width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cam_height)

        self.classifier = Classify()

    def start(self, cam_buffer, detection_buffer, center_buffer, area_buffer):
        out = None

        while True:
            ret, frame = self.cap.read()

            # Put frames in the camera buffer if the Myriad detector has already pulled it.
            if cam_buffer.empty():
                cam_buffer.put(frame)
            # Pull from the detection_buffer
            if not detection_buffer.empty():
                out = detection_buffer.get()
            # Classify the frame with the pulled detection
            if out is not None:
                frame = self.classifier.process_detection(frame, out, center_buffer, area_buffer)

            cv.imshow('Object Detection', frame)
            
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
                
        self.cap.release()
        cv.destroyAllWindows()
