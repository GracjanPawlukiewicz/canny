import cv2

class TargetImage:
    def __init__(self):
        self.scale_ratio = None
        self.target = None
        self.processed = None
        self.extension = None
        self.video = False

    def __call__(self, path):
        self.target = cv2.imread(path)
        self.extension = path.split('.')[-1]

    def canny_filter(self, thresholds):
        self.processed = cv2.Canny(self.target, thresholds[0], thresholds[1])

    def save(self, path):
        cv2.imwrite(path, self.processed)

    def show_preview(self):
        if self.processed is not None:
            cv2.imshow('Processed ', self.processed)


