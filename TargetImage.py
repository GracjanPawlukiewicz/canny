import cv2


class TargetImage:
    def __init__(self):
        self.scale_ratio = None
        self.photo = None

    def __call__(self, path):
        self.photo = cv2.imread(path)

    def canny_filter(self, lower_threshold, upper_threshold):
        return cv2.Canny(self.photo, lower_threshold, upper_threshold)

    def set_scale(self, scale):
        self.scale_ratio = scale

    def resize(self, image=None):
        if image is None:
            image_shape = self.photo.shape
            resized_image = cv2.resize(self.photo,
                                       [int(image_shape[1] * self.scale_ratio), int(image_shape[0] * self.scale_ratio)])
        else:
            image_shape = image.shape
            resized_image = cv2.resize(image,
                                       [int(image_shape[1] * self.scale_ratio),
                                        int(image_shape[0] * self.scale_ratio)])
        return resized_image
