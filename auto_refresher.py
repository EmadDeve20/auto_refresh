from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
import sys

class AutoRefresher(QtWidgets.QMainWindow):
    def __init__(self):
        super(AutoRefresher, self).__init__()
        uic.loadUi("./autorefresher.ui", self)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AutoRefresher()
    main_window.show()
    app.exec()