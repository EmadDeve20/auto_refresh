from PyQt5 import QtWidgets, uic
from PyQt5 import QtGui
from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool
from selenium import webdriver
import sys
import time
import traceback
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
        
        worker = Worker(self.run)
        self.qthread_pool.start(worker)

    def run(self):

        url = self.urlLineEdit.text()
        self.web_driver =  self.browsers[self.browsersCombo.currentIndex()]()
        period = int(self.periodEdt.text())
        self.web_driver.get(url)
        
        run_time = time.time()

        while True:
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
    
    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        if self.web_driver != None:
            self.web_driver.close()
        return super().closeEvent(a0)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main_window = AutoRefresher()
    main_window.show()
    app.exec()