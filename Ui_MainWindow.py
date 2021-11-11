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

from TargetImage import TargetImage
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QFileDialog, QMessageBox


class Ui_MainWindow(object):
    def __init__(self):
        self.image = None
        self.video = None
        self.processed_path = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(801, 605)
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

        self.leftSlider = QtWidgets.QSlider(self.centralwidget)
        self.leftSlider.setGeometry(QtCore.QRect(650, 370, 71, 160))
        self.leftSlider.setMaximum(600)
        self.leftSlider.setOrientation(QtCore.Qt.Vertical)
        self.leftSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.leftSlider.setObjectName("leftSlider")
        self.leftSlider.setVisible(False)

        self.rightSlider = QtWidgets.QSlider(self.centralwidget)
        self.rightSlider.setGeometry(QtCore.QRect(720, 369, 61, 161))
        self.rightSlider.setMaximum(600)
        self.rightSlider.setProperty("value", 80)
        self.rightSlider.setOrientation(QtCore.Qt.Vertical)
        self.rightSlider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.rightSlider.setObjectName("rightSlider")
        self.rightSlider.setVisible(False)

        self.selectFileButton = QtWidgets.QPushButton(self.centralwidget)
        self.selectFileButton.setGeometry(QtCore.QRect(360, 250, 75, 23))
        self.selectFileButton.setObjectName("selectFileButton")
        self.selectFileButton.clicked.connect(self.browseFiles)

        self.leftSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.leftSpinBox.setGeometry(QtCore.QRect(660, 540, 42, 22))
        self.leftSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.leftSpinBox.setMaximum(600)
        self.leftSpinBox.setObjectName("leftSpinBox")
        self.leftSpinBox.setVisible(False)

        self.rightSpinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.rightSpinBox.setGeometry(QtCore.QRect(730, 540, 42, 22))
        self.rightSpinBox.setButtonSymbols(QtWidgets.QAbstractSpinBox.NoButtons)
        self.rightSpinBox.setMaximum(600)
        self.rightSpinBox.setObjectName("rightSpinBox")
        self.rightSpinBox.setVisible(False)

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
        self.leftSlider.raise_()
        self.rightSlider.raise_()
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
        self.actionSaveFile = QtWidgets.QAction(MainWindow)
        self.actionSaveFile.setObjectName("actionSaveFile")

        self.actionAutoProcessing = QtWidgets.QAction(MainWindow)
        self.actionAutoProcessing.setObjectName("actionAutoProcessing")
        self.fileMenu.addAction(self.actionOpenFile)
        self.fileMenu.addAction(self.actionSaveFile)
        self.fileMenu.addAction(self.actionAutoProcessing)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())
        self.retranslateUi(MainWindow)
        self.selectFilterWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.processButton.setText(_translate("MainWindow", "Przetwarzaj"))
        self.processButton.clicked.connect(self.process)
        self.selectFileButton.setText(_translate("MainWindow", "Wybierz plik"))
        self.selectFilterWidget.setTabText(self.selectFilterWidget.indexOf(self.tab), _translate("MainWindow", "1"))
        self.selectFilterWidget.setTabText(self.selectFilterWidget.indexOf(self.tab_2), _translate("MainWindow", "+"))

        self.fileMenu.setTitle(_translate("MainWindow", "Plik"))
        self.helpMenu.setTitle(_translate("MainWindow", "Pomoc"))
        self.actionOpenFile.setText(_translate("MainWindow", "Otwórz plik"))
        self.actionOpenFile.triggered.connect(self.browseFiles)
        self.actionSaveFile.setText(_translate("MainWindow", "Zapisz plik"))
        self.actionAutoProcessing.setText(_translate("MainWindow", "Auto-przetwarzanie"))

    def browseFiles(self):
        file_explorer = QFileDialog.getOpenFileNames(filter="Images (*.jpg *.jpeg *.jpe *.jif *.jfif *.jfi *.gif *.png *.bmp);;"
                                                            "Videos (*.mp4 *.mov *.wmv *.avi *.avchd *.f4v *.flv *.swf *.m4p *.m4v);;"
                                                            "All files (*.*)")

        if not file_explorer[0]:
            self.showDialog("Nie wybrano żadnego pliku")
            return False

        elif len(file_explorer[0]) > 1:
            self.showDialog("Wybrano więcej niż jeden plik! \nTylko pierwszy z plików będzie używany")

        self.processed_path = file_explorer[0][0]
        self.checkPath()

    def showDialog(self, text):
        warning_message = QMessageBox()
        warning_message.setIcon(QMessageBox.Information)
        warning_message.setWindowTitle("Uwaga!")
        warning_message.setText(text)
        warning_message.exec_()

    def process(self):
        print(self.image)
        filters_dict = {"canny": self.image.cannyFilter}
        filters_arg = {"canny": [self.rightSlider.value(), self.leftSlider.value()]}

        for filter in filters_dict:
            filters_dict[filter](filters_arg[filter][0], filters_arg[filter][1])
        # TODO:
        #   -fix that
        shape = self.image.processed.shape
        print(shape)
        bytesPerLine = 3 * shape[1]
        # if len(shape == 3):
        #     qImg = QImage(self.image.processed.data, shape[1], shape[0], bytesPerLine,
        #                   QImage.Format_RGB888).rgbSwapped()
        # else:
        qImg = QImage(self.image.processed.data, shape[1], shape[0], bytesPerLine, QImage.Format_RGB888)
        pixmap = QPixmap(qImg)
        self.processedView.setPixmap(pixmap)

        # if self.image:
        #     #ADD HERE PROCESSING BY DICTIONARY
        #     self.image.cannyFilter()
        #     #update preview
        #     # height width channel



    def checkPath(self):
        mime = magic.Magic(mime=True)
        filename = mime.from_file(self.processed_path)

        if filename.find('video') != -1:
            print('it is video')

        elif filename.find('image') != -1:
            print('it is image')
            self.image = TargetImage()
            self.image(path=self.processed_path)
            self.video = None

            self.originalView.setVisible(True)
            self.processedView.setVisible(True)

            self.originalView.setScaledContents(True)
            self.processedView.setScaledContents(True)

            height, width, channel = self.image.photo.shape
            bytesPerLine = 3 * width
            qImg = QImage(self.image.photo.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            pixmap = QPixmap(qImg)
            self.originalView.setPixmap(pixmap)
            self.processedView.setPixmap(pixmap)

        else:
            self.showDialog("Wybrano niepoprawny format pliku!")
            return False

        self.selectFileButton.setVisible(False)
        self.selectFilterWidget.setVisible(True)
        self.rightSlider.setVisible(True)
        self.leftSlider.setVisible(True)
        self.processButton.setVisible(True)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
