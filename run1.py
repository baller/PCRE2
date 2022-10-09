# coding=utf-8
import sys
from camer import Ui_MainWindow
from PyQt5.QtWidgets import QApplication,QMainWindow,QPushButton,QWidget

from PyQt5.QtCore import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import QThread,QPixmap,QImage
import cv2
import time


class Thread1(QThread):  # 线程1
    sinOut1=pyqtSignal()
    def __init__(self):
        super().__init__()
        self.m=False
    def run(self):
        while self.m:
            if cv2.waitKey(100) & 0xff == ord('q'):
                break
            self.sinOut1.emit()

class Thread2(QThread):  # 线程2
    sinOut2=pyqtSignal()
    def __init__(self):
        super().__init__()
        self.m = False
    def run(self):
        while self.m:
            if cv2.waitKey(100) & 0xff == ord('q'):
                break
            self.sinOut2.emit()


class Camer1(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(Camer1,self).__init__(parent=None)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.cam_show1)
        self.pushButton_2.clicked.connect(self.cam_show2)
        self.thread1 = Thread1()
        self.thread1.sinOut1.connect(self.show1)
        self.thread2 = Thread2()
        self.thread2.sinOut2.connect(self.show2)
        self.camera1 = cv2.VideoCapture(0)
        self.camera2 = cv2.VideoCapture('rtsp://admin:admin@192.168.43.1:8554/live')
    def cam_show1(self):

        self.thread1.m= bool(1 - int(self.thread1.m))
        self.thread1.start()


    def cam_show2(self):
        self.thread2.m = bool(1 - int(self.thread2.m))
        self.thread2.start()

    def show1(self):

        ret, frame = self.camera1.read()
        frame = cv2.resize(frame, (480, 640), interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        frame = QImage(img, x, y, QImage.Format_RGB888)
        # pix = QPixmap.fromImage(frame)

        size = QSize(480, 640)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))

        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setPixmap(pix)


    def show2(self):

        ret, frame = self.camera2.read()
        print(2)
        frame = cv2.resize(frame, (480, 640), interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        x = img.shape[1]  # 获取图像大小
        y = img.shape[0]
        frame = QImage(img, x, y, QImage.Format_RGB888)
        # pix = QPixmap.fromImage(frame)

        size = QSize(480, 640)
        pix = QPixmap.fromImage(frame.scaled(size, QtCore.Qt.IgnoreAspectRatio))

        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setPixmap(pix)




if __name__=="__main__":
    app=QApplication(sys.argv)
    ui=Camer1()
    ui.show()
    sys.exit(app.exec_())