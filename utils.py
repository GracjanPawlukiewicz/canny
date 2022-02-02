from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QMessageBox, QFileDialog


def show_info_dialog(text):
    info_message = QMessageBox()
    info_message.setIcon(QMessageBox.Information)
    info_message.setWindowTitle("Uwaga!")
    info_message.setText(text)
    print("CWKS")
    info_message.exec_()


def open_save_explorer(target, filter_string):
    path = QFileDialog.getSaveFileName(filter=filter_string)

    print("duuupa")
    print("duuupa")
    print("duuupa")
    print("duuupa")
    print("duuupa")
    # empty returned path
    if path[0] == '':
        save_path = None

    # returned path got extension matching file_type
    elif path[0].split('.')[-1] in filter_string:
        split_path = path[0].split('.')
        target.extension = split_path[-1]
        path = split_path[:-1][0]
        save_path = '.'.join([path, target.extension])

    # returned path doesn't have extension in it
    else:
        save_path = '.'.join([path, target.extension])

    return save_path


def update_preview(source, preview):
    shape = source.shape

    if len(shape) > 2:
        bytes_per_line = 3 * shape[1]
        q_img = QImage(source.data, shape[1], shape[0], bytes_per_line,
                       QImage.Format_RGB888).rgbSwapped()

    else:
        q_img = QImage(source.data, shape[1], shape[0],
                       QImage.Format_Grayscale8)

    pixmap = QPixmap(q_img)
    preview.setPixmap(pixmap)
