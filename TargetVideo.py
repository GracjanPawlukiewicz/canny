import cv2

from ProgressBar import ProgressBar
from Worker import Worker


def canny_filter_thread(thresholds, target, change_value, finished):
    processed = []
    target_length = len(target)
    for count, frame in enumerate(target):
        processed.append(cv2.Canny(frame, thresholds[0], thresholds[1]))
        change_value.emit((count * 100) / target_length)
    change_value.emit(100)
    finished.emit(processed)


class TargetVideo:
    def __init__(self):
        self.target = []
        self.processed = []
        self.fps = None
        self.extension = None
        self.grayscale = False
        self.video = True

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

    def thread_complete(self, array):
        self.processed = array
        self.progress_bar.destroy()

    def show_preview(self):
        for frame in self.processed:
            cv2.imshow('Processed ', frame)
            if cv2.waitKey(25) & 0xFF == ord('q'):
                break

    def canny_filter(self, thresholds):
        self.progress_bar = ProgressBar()
        self.worker = Worker(values=thresholds, source=self.target, func=canny_filter_thread)
        self.worker.finished.connect(self.thread_complete)
        self.worker.change_value.connect(self.progress_bar.on_count_changed)
        self.worker.start()

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

