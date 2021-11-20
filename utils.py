from PIL import Image, ImageTk
import cv2
from PyQt5.QtGui import QImage, QPixmap


def update_preview(image, preview):
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
