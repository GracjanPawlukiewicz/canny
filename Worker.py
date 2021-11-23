from PyQt5.QtCore import QThread, pyqtSignal


class Worker(QThread):
    def __init__(self, func, values, source):
        super(Worker, self).__init__()
        self.values = values
        self.source = source
        self.func = func

    finished = pyqtSignal(list)
    change_value = pyqtSignal(float)

    def run(self):
        self.func(self.values, self.source, self.change_value, self.finished)

