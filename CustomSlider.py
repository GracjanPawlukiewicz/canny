# from PyQt5 import QtCore, QtWidgets
# from PyQt5.QtWidgets import QAbstractSpinBox
#
#
# class CustomSlider(QtWidgets.QWidget):
#     def __init__(self, window, geometry, *args, **kwargs):
#         super(CustomSlider, self).__init__(*args, **kwargs)
#         self.slider = QtWidgets.QSlider(QtCore.Qt.Vertical)
#         self.slider.valueChanged.connect(self.handleSliderValueChange)
#         self.slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
#
#         self.numbox = QtWidgets.QSpinBox()
#         self.numbox.setButtonSymbols(QAbstractSpinBox.NoButtons)
#         self.numbox.valueChanged.connect(self.handleNumboxValueChange)
#
#         layout = QtWidgets.QVBoxLayout(window)
#         layout.setGeometry(geometry)
#         layout.setAlignment(QtCore.Qt.AlignCenter)
#         layout.addWidget(self.slider)
#         layout.addWidget(self.numbox)
#
#     @QtCore.pyqtSlot(int)
#     def handleSliderValueChange(self, value):
#         self.numbox.setValue(value)
#
#     @QtCore.pyqtSlot(int)
#     def handleNumboxValueChange(self, value):
#         # Prevent values outside slider range
#         if value < self.slider.minimum():
#             self.numbox.setValue(self.slider.minimum())
#         elif value > self.slider.maximum():
#             self.numbox.setValue(self.slider.maximum())
#
#         self.slider.setValue(self.numbox.value())
#
# # app = QtWidgets.QApplication([])
# # slider1 = CustomSlider()
# # slider2 = CustomSlider()
# # window = QtWidgets.QWidget()
# # layout = QtWidgets.QVBoxLayout(window)
# # layout.addWidget(slider1)
# # layout.addWidget(slider2)
# # window.show()
# # app.exec_()

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QAbstractSpinBox


class CustomSlider(QtWidgets.QWidget):
    def __init__(self, window, geometry, *args, **kwargs):
        super(CustomSlider, self).__init__(*args, **kwargs)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Vertical)

        self.numbox = QtWidgets.QSpinBox()
        self.numbox.setRange(self.slider.minimum(), self.slider.maximum())
        self.numbox.setButtonSymbols(QAbstractSpinBox.NoButtons)

        self.slider.valueChanged.connect(self.numbox.setValue)
        self.slider.rangeChanged.connect(self.numbox.setRange)

        self.numbox.valueChanged.connect(self.slider.setValue)

        layout = QtWidgets.QVBoxLayout(window)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setGeometry(geometry)
        layout.addWidget(self.slider)
        layout.addWidget(self.numbox)

    @QtCore.pyqtSlot(int)
    def setMinimum(self, minval):
        self.slider.setMinimum(minval)

    @QtCore.pyqtSlot(int)
    def setMaximum(self, maxval):
        self.slider.setMaximum(maxval)

    @QtCore.pyqtSlot(int, int)
    def setRange(self, minval, maxval):
        self.slider.setRange(minval, maxval)

    @QtCore.pyqtSlot(int)
    def setValue(self, value):
        self.slider.setValue(value)