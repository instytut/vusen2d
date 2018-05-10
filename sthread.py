from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import time

class MainWindow(QMainWindow):


    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.counter = 0
        self.image = QImage(800, 600, QImage.Format_RGB32)
        self.image.fill(Qt.white)

        layout = QVBoxLayout()

        self.l = QLabel("Start")
        self.l.setAlignment(Qt.AlignCenter)
        if not self.image.isNull():
            self.l.setPixmap(QPixmap.fromImage(self.image).scaled(self.l.size(),Qt.KeepAspectRatio,Qt.FastTransformation))

        layout.addWidget(self.l)

        w = QWidget()
        w.setLayout(layout)

        self.setCentralWidget(w)

        self.show()

        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.recurring_timer)
        self.timer.start()

    def oh_no(self):
        time.sleep(5)

    def recurring_timer(self):
        self.counter +=1
        qp = QPainter()
        qp.begin(self.image)
        pen = QPen(Qt.black, 2, Qt.SolidLine)
        qp.setPen(pen)
        qp.drawLine(20, 20, 100, 100+self.counter)
        qp.end()
        #if not self.image.isNull():
        self.l.setPixmap(QPixmap.fromImage(self.image).scaled(self.l.size(),Qt.KeepAspectRatio,Qt.FastTransformation))
        self.l.setText("Counter: %d" % self.counter)
        self.update()


app = QApplication([])
window = MainWindow()
app.exec_()