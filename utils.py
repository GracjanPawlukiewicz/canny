from PIL import Image, ImageTk
import cv2
from PyQt5.QtGui import QImage, QPixmap


def opencvToPIL(image):
    """Method that converts photo from opencv array to PIL image instance

        Arguments:
            image - image that is going to be converted

        :return PIL image
    """
    if len(image.shape) > 2:
        b, g, r = cv2.split(image)
        img = cv2.merge((r, g, b))
        im = Image.fromarray(img)
    else:
        im = Image.fromarray(image)

    pil_image = ImageTk.PhotoImage(im)
    return pil_image


def getScaleRatio(shape, height, width, image_placement):
    """ Method calculates image scale to fit into window

        Arguments:
            shape - image shape in opencv array format [height, width, number of channels]
            height - main window height
            width - main window width
            image_placement - processed image placement on window [X, Y]
    """
    img_new_height = height - image_placement[1]
    height_scale_ratio = img_new_height / shape[0]
    img_new_width = width - (image_placement[0] * 2)
    width_scale_ratio = img_new_width / shape[1]

    if height_scale_ratio >= width_scale_ratio:
        return width_scale_ratio
    else:
        return height_scale_ratio

def updatePreview(image, preview):
    shape = image.shape

    if len(shape) > 2:
        bytesPerLine = 3 * shape[1]
        qImg = QImage(image.data, shape[1], shape[0], bytesPerLine,
                      QImage.Format_RGB888).rgbSwapped()

    else:
        qImg = QImage(image.data, shape[1], shape[0],
                      QImage.Format_Grayscale8)

    pixmap = QPixmap(qImg)
    preview.setPixmap(pixmap)
