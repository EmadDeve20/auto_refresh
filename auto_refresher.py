from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
from selenium import webdriver
import sys
import time
import traceback
import selenium

class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.
    Supported signals are:
    finished
        No data
    error
        tuple (exctype, value, traceback.format_exc() )
    result
        object data returned from processing, anything
    progress
        int indicating % progress
    '''
    finished = pyqtSignal()
    error = pyqtSignal(tuple)
    result = pyqtSignal(object)
    progress = pyqtSignal(int)


class Worker(QRunnable):
    '''
    Worker thread
    Inherits from QRunnable to handler worker thread setup, signals and wrap-up.
    :param callback: The function callback to run on this worker thread. Supplied args and
                     kwargs will be passed through to the runner.
    :type callback: function
    :param args: Arguments to pass to the callback function
    :param kwargs: Keywords to pass to the callback function
    '''

    def __init__(self, fn, *args, **kwargs):
        super(Worker, self).__init__()

        # Store constructor arguments (re-used for processing)
        self.fn = fn
        self.args = args
        self.kwargs = kwargs
        self.signals = WorkerSignals()

    @pyqtSlot()
    def run(self):
        '''
        Initialise the runner function with passed args, kwargs.
        '''

        # Retrieve args/kwargs here; and fire processing using them
        try:
            result = self.fn(*self.args, **self.kwargs)
        except:
            traceback.print_exc()
            exctype, value = sys.exc_info()[:2]
            self.signals.error.emit((exctype, value, traceback.format_exc()))
        else:
            # Return the result of the processing
            self.signals.result.emit(result)
        finally:
            self.signals.finished.emit()  # Done

class AutoRefresher(QtWidgets.QMainWindow):
    def __init__(self):
        super(AutoRefresher, self).__init__()
        uic.loadUi("./autorefresher.ui", self)
        self.web_driver = None
        self.startBtn.clicked.connect(self.create_thread_autorefresher)
        self.qthread_pool = QThreadPool()
    
    def create_thread_autorefresher(self):
        
        if (self.startBtn.text() == "Start"):
            self.change_start_button_text()
            worker = Worker(self.run)
            worker.signals.finished.connect(self.change_start_button_text)
            self.qthread_pool.start(worker)
        
        elif (self.startBtn.text() == "Stop"):
            if (self.web_driver != None):
                self.web_driver.close()

        
    def change_start_button_text(self):
        if (self.startBtn.text() == "Start"):
            self.startBtn.setText("Stop")
        elif (self.startBtn.text() == "Stop"):
            self.startBtn.setText("Start")
            

    def run(self):

        self.infoLabel.setText("")

        url = self.urlLineEdit.text()
        self.web_driver =  self.browsers[self.browsersCombo.currentIndex()]()
        period = int(self.periodEdt.text())
        
        try:
            self.web_driver.get(url)
        except selenium.common.exceptions.InvalidArgumentException:
            self.infoLabel.setText("Invalid Url!")
            self.web_driver.close()
            return

        run_time = time.time()

        while self.web_driver.window_handles:
            if (self.curentTime - run_time) >= period:
                self.web_driver.refresh()
                run_time = self.curentTime

    @property
    def browsers(self):
        return [
            webdriver.Chrome,
            webdriver.Firefox,
            webdriver.Ie,
        ]
    
    @property
    def curentTime(self):
        return time.time()
    


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AutoRefresher()
    main_window.show()
    app.exec()