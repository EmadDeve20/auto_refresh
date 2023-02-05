from PyQt5 import QtWidgets, uic
from PyQt5 import QtCore
from selenium import webdriver
import sys
import time

class AutoRefresher(QtWidgets.QMainWindow):
    def __init__(self):
        super(AutoRefresher, self).__init__()
        uic.loadUi("./autorefresher.ui", self)

        self.startBtn.clicked.connect(self.run)
    
    def run(self):

        url = self.urlLineEdit.text()
        web_driver =  self.browsers[self.browsersCombo.currentIndex()]()
        period = int(self.periodEdt.text())

        while True:
            web_driver.get(url)
            time.sleep(period)

    @property
    def browsers(self):
        return [
            webdriver.Chrome,
            webdriver.Firefox,
            webdriver.Ie,
        ]


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AutoRefresher()
    main_window.show()
    app.exec()