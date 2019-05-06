import cv2 as cv


class Detect:
    def __init__(self, myriad):
        self.net = None
        if myriad:
            self._start_myriad()

    def _start_myriad(self):
        self.net = cv.dnn.readNet('frozen_inference_graph.xml', 'frozen_inference_graph.bin')
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

    def start(self, cam_buffer, detection_buffer):
        while True:
            if not cam_buffer.empty():
                frame = cam_buffer.get()
                blob = cv.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv.CV_8U)
                self.net.setInput(blob)
                out = self.net.forward()
                detection_buffer.put(out)
