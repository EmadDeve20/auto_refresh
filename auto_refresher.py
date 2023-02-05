from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from selenium import webdriver
import sys
import time

class AutoRefresher(QtWidgets.QMainWindow):
    def __init__(self):
        super(AutoRefresher, self).__init__()
        uic.loadUi("./autorefresher.ui", self)
        self.web_driver = None
        self.startBtn.clicked.connect(self.run)
    
    def run(self):

        url = self.urlLineEdit.text()
        self.web_driver =  self.browsers[self.browsersCombo.currentIndex()]()
        period = int(self.periodEdt.text())

        while True:
            self.web_driver.get(url)
            time.sleep(period)

    @property
    def browsers(self):
        return [
            webdriver.Chrome,
            webdriver.Firefox,
            webdriver.Ie,
        ]
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.web_driver != None:
            self.web_driver.close()
        return super().closeEvent(a0)



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AutoRefresher()
    main_window.show()
    app.exec()