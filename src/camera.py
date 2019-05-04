import cv2 as cv
import time

class Camera:
    def __init__(self, cam_width=320, cam_height=240):
        self.cap = cv.VideoCapture(0)
        self.cap.set(cv.CAP_PROP_FRAME_WIDTH, cam_width)
        self.cap.set(cv.CAP_PROP_FRAME_HEIGHT, cam_height)

    def start_camera(self, cam_buffer, detection_buffer, center_buffer, area_buffer):
        out = None

        while True:
            ret, frame = self.cap.read()

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

                if area is None:
                    saber.stop()

                center = None
                area = None

            cv.imshow('frame', frame)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break
        self.cap.release()
        cv.destroyAllWindows()


def image_overlay(image, details):
    overlay = image
    label_font = cv.FONT_HERSHEY_SIMPLEX

    xy_min = details[0]
    xy_max = details[1]
    center = details[2]
    confidence = details[3]

    cv.rectangle(overlay, xy_min, xy_max, color=(0, 255, 0))
    cv.circle(overlay, center, 4, (255, 0, 0), 2)
    cv.putText(overlay, 'piggy: ' + str(round(confidence, 2) * 100) + '%', (xy_min[0] + 2, xy_min[1] + 10), label_font,
               0.3, (255, 255, 255), 1, cv.LINE_AA)
    return overlay