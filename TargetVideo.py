import cv2
import numpy as np

class TargetVideo:
    def __init__(self):
        self.target = []
        self.processed = []
        self.fps = None
        self.extension = None
        self.grayscale = False

    def __call__(self, path):
        cap = cv2.VideoCapture(path)
        self.fps = int(cap.get(cv2.CAP_PROP_FPS))
        self.extension = path.split('.')[-1]

        while cap.isOpened():
            # Capture frame-by-frame
            ret, frame = cap.read()

            if ret:
                self.target.append(frame)
            else:
                break
        cap.release()

    def canny_filter(self, thresholds):
        for frame in self.target:
            self.processed.append(cv2.Canny(frame, thresholds[0], thresholds[1]))

    def save(self, path):
        video_shape = self.processed[0].shape
        fourcc = cv2.VideoWriter_fourcc(*'FMP4')

        # BGR video
        if len(video_shape) > 2:
                                                            #   Width           Height
            out = cv2.VideoWriter(path, fourcc, self.fps, (video_shape[1], video_shape[0]))
        # Grayscale video
        else:
                                                            #   Width           Height
            out = cv2.VideoWriter(path, fourcc, self.fps, (video_shape[1], video_shape[0]), 0)
        for frame in self.processed:
            out.write(frame)

