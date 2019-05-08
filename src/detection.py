import cv2 as cv


class Detect:
    def __init__(self, myriad):
        self.net = None
        if myriad:
            self._start_myriad()

    def _start_myriad(self):
        # Read in the Intermediate Representation files. Note: upon creating a new model, replace these files within
        # the source folder and/or adjust the filenames below.
        self.net = cv.dnn.readNet('frozen_inference_graph.xml', 'frozen_inference_graph.bin')
        # Set the inference device to Myriad/NCS2
        self.net.setPreferableTarget(cv.dnn.DNN_TARGET_MYRIAD)

    def start(self, cam_buffer, detection_buffer):
        while True:
            if not cam_buffer.empty():
                frame = cam_buffer.get()
                blob = cv.dnn.blobFromImage(frame, size=(300, 300), ddepth=cv.CV_8U)
                self.net.setInput(blob)
                out = self.net.forward()
                detection_buffer.put(out)


class Classify:

    def process_detection(self, frame, out, center_buffer, area_buffer):
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
                frame = self._image_overlay(frame, detection_details)

        return frame

    def _image_overlay(self, image, details):
        overlay = image
        label_font = cv.FONT_HERSHEY_SIMPLEX

        xy_min = details[0]
        xy_max = details[1]
        center = details[2]
        confidence = details[3]

        cv.rectangle(overlay, xy_min, xy_max, color=(0, 255, 0))
        cv.circle(overlay, center, 4, (255, 0, 0), 2)
        cv.putText(overlay, 'piggy: ' + str(round(confidence, 2) * 100) + '%', (xy_min[0] + 2, xy_min[1] + 10),
                   label_font,
                   0.3, (255, 255, 255), 1, cv.LINE_AA)
        return overlay