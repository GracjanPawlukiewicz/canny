import time

import magic
import sys

from TargetImage import TargetImage

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QSizePolicy
from qtrangeslider import QRangeSlider

from TargetVideo import TargetVideo
from utils import update_preview, show_info_dialog, open_save_explorer

SLIDER_RANGE = 600
IMAGES_FORMATS = "Images (*.jpg *.jpeg *.jpe *.jif *.jfif *.jfi *.gif *.png *.bmp);;"
VIDEOS_FORMATS = "Videos (*.mp4 *.mov *.wmv *.avi *.avchd *.f4v *.flv *.swf *.m4p *.m4v);;"

#TODO:
#   -add comments (XD)
#   -show video preview
#   -enable auto-processing for images
#   -add other filters


class UiMainWindow(object):
    def __init__(self):
        self.source = None
        self.already_saved = False

    def setup_ui(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(801, 605)
        self.centralwidget = QtWidgets.QWidget(main_window)
        self.centralwidget.setObjectName("centralwidget")

        self.processButton = QtWidgets.QPushButton(self.centralwidget)
        self.processButton.setGeometry(QtCore.QRect(360, 350, 75, 23))
        self.processButton.setObjectName("processButton")
        self.processButton.setVisible(False)

        self.previewButton = QtWidgets.QPushButton(self.centralwidget)
        self.previewButton.setGeometry(QtCore.QRect(360, 450, 75, 23))
        self.previewButton.setObjectName("processButton")
        self.previewButton.setVisible(False)

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

        main_window.setCentralWidget(self.centralwidget)

        self.menubar = QtWidgets.QMenuBar(main_window)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 801, 21))
        self.menubar.setObjectName("menubar")
        self.fileMenu = QtWidgets.QMenu(self.menubar)
        self.fileMenu.setObjectName("menuPlik")
        self.helpMenu = QtWidgets.QMenu(self.menubar)
        self.helpMenu.setObjectName("menuPomoc")
        main_window.setMenuBar(self.menubar)

        self.statusbar = QtWidgets.QStatusBar(main_window)
        self.statusbar.setObjectName("statusbar")
        main_window.setStatusBar(self.statusbar)

        self.actionOpenFile = QtWidgets.QAction(main_window)
        self.actionOpenFile.setObjectName("actionOpenFile")
        self.actionOpenFile.setShortcut("Ctrl+O")
        self.actionOpenFile.triggered.connect(self.get_file_path)

        self.actionSaveFile = QtWidgets.QAction(main_window)
        self.actionSaveFile.setObjectName("actionSaveFile")
        self.actionSaveFile.setShortcut("Ctrl+S")
        self.actionSaveFile.setStatusTip('Save File')
        self.actionSaveFile.triggered.connect(self.save_file)

        self.actionAutoProcessing = QtWidgets.QAction(main_window)
        self.actionAutoProcessing.setObjectName("actionAutoProcessing")
        self.fileMenu.addAction(self.actionOpenFile)
        self.fileMenu.addAction(self.actionSaveFile)
        self.fileMenu.addAction(self.actionAutoProcessing)

        self.menubar.addAction(self.fileMenu.menuAction())
        self.menubar.addAction(self.helpMenu.menuAction())
        self.retranslate_ui(main_window)
        self.selectFilterWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def save_file(self):
        if self.source is None:
            show_info_dialog("Brak pliku do zapisu!")
            return False

        elif self.source:
            #TODO:
            #   -figure out why source.processed gives exception for image even when it gots it
            if len(self.source.processed) > 0:

                if self.source.video:
                    save_path = open_save_explorer(target=self.source,
                                                   filter_string=VIDEOS_FORMATS)

                else:
                    save_path = open_save_explorer(target=self.source,
                                                   filter_string=IMAGES_FORMATS)

                if save_path:
                    self.source.save(save_path)
                else:
                    show_info_dialog("Nie podano ścieżki \nAnulowano zapis pliku!")
            else:
                show_info_dialog("Brak pliku do zapisu!")


    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "MainWindow"))
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

    def get_file_path(self):
        path = QFileDialog.getOpenFileNames(
            filter=IMAGES_FORMATS +
                   VIDEOS_FORMATS +
                   "All files (*.*)")

        if not path[0]:
            show_info_dialog("Nie wybrano żadnego pliku")
            return False

        elif len(path[0]) > 1:
            show_info_dialog("Wybrano więcej niż jeden plik! \nTylko pierwszy z plików będzie używany")

        self.load_file(path[0][0])

    def process_target(self):
        # CHANGE TO VIDEO!!!
        filters_dict = {"canny": self.source.canny_filter}
        filters_arg = {"canny": self.rangeSlider.value()}

        for filter_name in filters_dict:
            filters_dict[filter_name](filters_arg[filter_name])

        if not self.source.video:
            update_preview(self.source.processed, self.processedView)
        else:
            self.previewButton.setVisible(True)


    def load_file(self, path):
        mime = magic.Magic(mime=True)
        filename = mime.from_file(path)

        if filename.find('video') != -1:
            self.previewButton.setVisible(False)
            self.source = TargetVideo()
            self.source(path=path)

            self.previewButton.clicked.connect(self.source.play_video)

            #Temporary disabling preview
            self.originalView.setVisible(False)
            self.processedView.setVisible(False)

            self.originalView.setScaledContents(False)
            self.processedView.setScaledContents(False)

            self.originalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.processedView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        elif filename.find('image') != -1:
            self.source = TargetImage()
            self.source(path=path)

            self.originalView.setVisible(True)
            self.processedView.setVisible(True)

            self.originalView.setScaledContents(True)
            self.processedView.setScaledContents(True)

            self.originalView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.processedView.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

            update_preview(self.source.target, self.originalView)
            update_preview(self.source.target, self.processedView)

        else:
            show_info_dialog("Wybrano niepoprawny format pliku!")
            return False

        self.selectFileButton.setVisible(False)
        self.selectFilterWidget.setVisible(True)
        self.rangeSlider.setVisible(True)
        self.rightSpinBox.setVisible(True)
        self.leftSpinBox.setVisible(True)
        self.processButton.setVisible(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = UiMainWindow()
    ui.setup_ui(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
