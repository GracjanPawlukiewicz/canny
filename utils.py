from PIL import Image, ImageTk
import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QFileDialog


def show_info_dialog(text):
    info_message = QMessageBox()
    info_message.setIcon(QMessageBox.Information)
    info_message.setWindowTitle("Uwaga!")
    info_message.setText(text)
    info_message.exec_()


def open_save_explorer(target, filter_string):
    path = QFileDialog.getSaveFileName(filter=filter_string)

    if path[0] == '':
        show_info_dialog("Nie podano ścieżki \nAnulowano zapis pliku!")

    elif path[0].split('.')[-1] in filter_string:
        split_path = path[0].split('.')
        target.extension = split_path[-1]
        print(target.extension)
        path = split_path[:-1][0]

    return path


def update_preview(image, preview):
    shape = image.shape

    if len(shape) > 2:
        bytes_per_line = 3 * shape[1]
        q_img = QImage(image.data, shape[1], shape[0], bytes_per_line,
                       QImage.Format_RGB888).rgbSwapped()

    else:
        q_img = QImage(image.data, shape[1], shape[0],
                       QImage.Format_Grayscale8)

    pixmap = QPixmap(q_img)
    preview.setPixmap(pixmap)
