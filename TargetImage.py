import cv2


class TargetImage:
    def __init__(self):
        self.scale_ratio = None
        self.target = None
        self.processed = None
        self.extension = None

    def __call__(self, path):
        self.target = cv2.imread(path)
        self.extension = path.split('.')[-1]

    def canny_filter(self, thresholds):
        self.processed = cv2.Canny(self.target, thresholds[0], thresholds[1])

    def resize_image(self, image=None, dimensions=None):
        if dimensions is None:
            dimensions = [100, 100]
        if image is None:
            image_shape = self.target.shape
            resized_image = cv2.resize(self.target,
                                       [int(image_shape[1] * self.scale_ratio), int(image_shape[0] * self.scale_ratio)])
        else:
            resized_image = cv2.resize(image, dimensions)
        return resized_image

    def save(self, path):
        cv2.imwrite(path, self.processed)


