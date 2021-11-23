import sys
import time

from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import (QApplication, QDialog,
                             QProgressBar, QPushButton)
from PyQt5.uic.properties import QtCore



class ProgressBar(QDialog):
    """
    Simple dialog that consists of a Progress Bar.
    """

    def __init__(self, ):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Przetwarzanie')
        self.resize(600, 30)

        self.progress = QProgressBar(self)
        self.progress.setGeometry(0, 2, 600, 25)

        self.show()

    def on_count_changed(self, value):
        self.progress.setValue(value)

