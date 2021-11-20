# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'canny.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
import imghdr
import magic
from PyQt5.QtGui import QPixmap, QImage
from qtrangeslider import QRangeSlider
import os

from CustomSlider import CustomSlider
from TargetImage import TargetImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox, QSizePolicy

from utils import update_preview

SLIDER_RANGE = 600
IMAGES_FORMATS = "Images (*.jpg *.jpeg *.jpe *.jif *.jfif *.jfi *.gif *.png *.bmp);;"
VIDEOS_FORMATS = "Videos (*.mp4 *.mov *.wmv *.avi *.avchd *.f4v *.flv *.swf *.m4p *.m4v);;"

class Ui_MainWindow(object):
    def __init__(self):
        self.image = None
        self.video = None
        self.processed_path = None
        self.already_saved = False

    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize_image(801, 605)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.processButton = QtWidgets.QPushButton(self.centralwidget)
        self.processButton.setGeometry(QtCore.QRect(360, 350, 75, 23))
        self.processButton.setObjectName("processButton")
        self.processButton.setVisible(False)

        self.originalView = QtWidgets.QLabel(self.centralwidget)
        self.originalView.setGeometry(QtCore.QRect(20, 10, 371, 321))
        self.originalView.setObjectName("originalView")
        self.originalView.setVisible(False)

        self.processedView = QtWidgets.QLabel(self.centralwidget)
        self.processedView.setGeometry(QtCore.QRect(410, 10, 371, 321))
        self.processedView.setObjectName("processedView")
        self.processedView.setVisible(False)

        self.rangeSlider = QRangeSlider(self.centralwidget)
        self.rangeSlider.setGeometry(QtCore.QRect(550, 450, 180, 20))
        self.rangeSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.rangeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.rangeSlider.setObjectName("rangeSlider")

        self.rangeSlider.setMinimum(0)
        self.rangeSlider.setMaximum(SLIDER_RANGE)
        self.rangeSlider.valueChanged.connect(self.update_spinboxes)
        self.rangeSlider.setVisible(False)


        self.leftSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.leftSpinBox.setGeometry(QtCore.QRect(520, 450, 25, 20))
        self.leftSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.leftSpinBox.setMaximum(600)
        self.leftSpinBox.setObjectName("leftSpinBox")
        self.leftSpinBox.setVisible(False)


        self.rightSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.rightSpinBox.setGeometry(QtCore.QRect(740, 450, 25, 20))
        self.rightSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rightSpinBox.setMaximum(600)
        self.rightSpinBox.setObjectName("rightSpinBox")
        self.rightSpinBox.setVisible(False)

        self.update_spinboxes()

        self.selectFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectFileButton.setGeometry(QtCore.QRect(360, 250, 75, 23))
        self.selectFileButton.setObjectName("selectFileButton")
        self.selectFileButton.clicked.connect(self.get_file_path)

        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(10, 0, 781, 341))
        self.frame.setAutoFillBackground(False)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.selectFilterWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.selectFilterWidget.setGeometry(QtCore.QRect(30, 420, 101, 111))
        self.selectFilterWidget.setObjectName("selectFilterWidget")
        self.selectFilterWidget.setVisible(False)

        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.selectFilterWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.selectFilterWidget.addTab(self.tab_2, "")

        self.frame.raise_()
        self.processButton.raise_()
        self.originalView.raise_()
        self.processedView.raise_()
        self.rangeSlider.raise_()
        self.selectFileButton.raise_()
        self.leftSpinBox.raise_()
        self.rightSpinBox.raise_()
        self.selectFilterWidget.raise_()

        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("menuPlik")
        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu.setObjectName("menuPomoc")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionOpenFile = QtWidgets.QAction(MainWindow)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionOpenFile.setShortcut("Ctrl+O")
        self.actionOpenFile.triggered.connect(self.get_file_path)


        self.actionSaveFile = QtWidgets.QAction(MainWindow)
        self.actionSaveFile.setObjectName("actionSaveFile")
        self.actionSaveFile.setShortcut("Ctrl+S")
        self.actionSaveFile.setStatusTip('Save File')
        self.actionSaveFile.triggered.connect(self.save_file)

        self.actionAutoProcessing = QtWidgets.QAction(MainWindow)
        self.actionAutoProcessing.setObjectName("actionAutoProcessing")
        self.fileMenu.addAction(self.actionOpenFile)
        self.fileMenu.addAction(self.actionSaveFile)
        self.fileMenu.addAction(self.actionAutoProcessing)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())
        self.retranslate_ui(MainWindow)
        self.selectFilterWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def save_file(self):
        if self.video is None and self.image is None:
            self.show_dialog("Brak pliku do zapisu!")
            return False

        elif self.video is None and self.image:
            if self.image.processed is None:
                self.show_dialog("Brak pliku do zapisu!")
            else:
                save_path = self.open_save_explorer(self.image.extension)
                save_path = '.'.join([save_path[0], self.image.extension])
                #TODO:
                #   -add check if file exist - then ask for overwrite

                print(save_path)
                self.image.save(save_path)

        elif self.image is None and self.video:
            if self.video.processed is None:
                self.show_dialog("Brak pliku do zapisu!")
            else:
                print("save video file")

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.processButton.setText(_translate("MainWindow", "Przetwarzaj"))
        self.processButton.clicked.connect(self.process_target)

        self.selectFileButton.setText(_translate("MainWindow", "Wybierz plik"))
        self.selectFilterWidget.setTabText(self.selectFilterWidget.indexOf(self.tab), _translate("MainWindow", "1"))
        self.selectFilterWidget.setTabText(self.selectFilterWidget.indexOf(self.tab_2), _translate("MainWindow", "+"))

        self.fileMenu.setTitle(_translate("MainWindow", "Plik"))
        self.helpMenu.setTitle(_translate("MainWindow", "Pomoc"))
        self.actionOpenFile.setText(_translate("MainWindow", "Otwórz plik"))
        self.actionSaveFile.setText(_translate("MainWindow", "Zapisz plik"))
        self.actionAutoProcessing.setText(_translate("MainWindow", "Auto-przetwarzanie"))

    def update_spinboxes(self):
        values = self.rangeSlider.value()
        self.leftSpinBox.setValue(values[0])
        self.leftSpinBox.setMaximum(values[1])

        self.rightSpinBox.setValue(values[1])
        self.rightSpinBox.setMinimum(values[0])

    def open_save_explorer(self, extension):
        file_explorer = QFileDialog.getSaveFileName(filter=f"Format (.{extension})")
        if file_explorer[0] == '':
            self.show_dialog("Anulowano zapis pliku!")
        return file_explorer

    def get_file_path(self):
        file_explorer = QFileDialog.getOpenFileNames(
            filter=IMAGES_FORMATS +
                   VIDEOS_FORMATS +
                   "All files (*.*)")

        if not file_explorer[0]:
            self.show_dialog("Nie wybrano żadnego pliku")
            return False

        elif len(file_explorer[0]) > 1:
            self.show_dialog("Wybrano więcej niż jeden plik! \nTylko pierwszy z plików będzie używany")

        self.processed_path = file_explorer[0][0]
        self.load_file()

    def show_dialog(self, text):
        warning_message = QMessageBox()
        warning_message.setIcon(QMessageBox.Information)
        warning_message.setWindowTitle("Uwaga!")
        warning_message.setText(text)
        warning_message.exec_()

    def process_target(self):
        print(self.image)
        filters_dict = {"canny": self.image.canny_filter}
        filters_arg = {"canny": self.rangeSlider.value()}

        for filter_name in filters_dict:
            filters_dict[filter_name](filters_arg[filter_name])
        # TODO:
        #   - fix processed preview
        print(self.processedView.size())
        print(self.originalView.size())

        # img = self.image.resize(image=self.image.processed, dimensions=[371, 321])

        update_preview(self.image.processed, self.processedView)

    def load_file(self):
        mime = magic.Magic(mime=True)
        filename = mime.from_file(self.processed_path)

        if filename.find('video') != -1:
            print('it is video')

        elif filename.find('image') != -1:
            self.image = TargetImage()
            self.image(path=self.processed_path)
            self.video = None

            self.originalView.setVisible(True)
            self.processedView.setVisible(True)

            self.originalView.setScaledContents(True)
            self.processedView.setScaledContents(True)

            self.originalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.processedView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            update_preview(self.image.photo, self.originalView)
            update_preview(self.image.photo, self.processedView)

        else:
            self.show_dialog("Wybrano niepoprawny format pliku!")
            return False

        self.selectFileButton.setVisible(False)
        self.selectFilterWidget.setVisible(True)
        self.rangeSlider.setVisible(True)
        self.rightSpinBox.setVisible(True)
        self.leftSpinBox.setVisible(True)
        self.processButton.setVisible(True)

if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
