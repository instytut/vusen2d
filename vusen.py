from PyQt5.QtWidgets import QWidget, QApplication, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QPen, QImage, QPixmap
from PyQt5.QtCore import Qt, QObject, pyqtSignal, pyqtSlot, QRunnable, QThreadPool, QTimer
import time
import traceback, sys

class Point:
    def __init__(self, x=0, y=0, color=0):
        self.x = x
        self.y = y
        self.color = color

    def __print__(self):
        print('(', self.x, ',', self.y, ':', self.color, ')')

    def draw(self, QPainter):
        pass



class Line:
    def __init__(self, p0, length=0, phi=0, color=0):
        pass






class WorkerSignals(QObject):
    '''
    Defines the signals available from a running worker thread.

    Supported signals are:

    finished
        No data

    error
        `tupleself.counter +=1
        qp = QPainter()
        qp.begin(self.image)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 20, 100, 100+self.counter)
        qp.end()` (exctype, value, traceback.format_exc() )

    result
        `object` data returned from processing, anything

    progress
        `int` indicating % progress

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
        # Add the callback to our kwargs
        kwargs['progress_callback'] = self.signals.progress

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
            self.signals.result.emit(result)  # Return the result of the processing
        finally:
            self.signals.finished.emit()  # Done

class MainWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.counter = 0
        self.image = QImage(800, 600, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        self.l.setAlignment(Qt.AlignCenter)

        b = QPushButton("DANGER!")
        b.pressed.connect(self.oh_no)

        layout.addWidget(self.l)
        layout.addWidget(b)


        self.setLayout(layout)

        self.initUI()

        self.threadpool = QThreadPool()
        print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def initUI(self):
        self.setGeometry(300, 300, 280, 270)
        self.setWindowTitle('Vusen 2D')
        self.show()

    def paintEvent(self, e):
        if not self.image.isNull():
            self.l.setPixmap(
                QPixmap.fromImage(self.image).scaled(self.l.size(), Qt.KeepAspectRatio, Qt.FastTransformation))

    def startPaint(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

    def progress_fn(self, n):
        print("%d%% done" % n)

    def execute_this_fn(self, progress_callback):
        for n in range(0, 5):
            time.sleep(1)
            progress_callback.emit(n*100/4)

        return "Done."

    def print_output(self, s):
        print(s)

    def thread_complete(self):
        print("THREAD COMPLETE!")

    def oh_no(self):
        # Pass the function to execute
        worker = Worker(self.execute_this_fn) # Any other args, kwargs are passed to the run function
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_complete)
        worker.signals.progress.connect(self.progress_fn)

        # Execute
        self.threadpool.start(worker)


    def recurring_timer(self):
        self.counter += 1
        qp = QPainter()
        qp.begin(self.image)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 20, 100, 100 + self.counter)
        qp.end()
        self.l.setText("Counter: %d" % self.counter)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())