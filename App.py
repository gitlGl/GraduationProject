import sys, os, psutil
from PyQt6.QtWidgets import QApplication
from src.OpenCapture import OpenCapture
from src.Process import *
from multiprocessing import Process, Queue
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtCore import pyqtSlot, QObject
from src.Ui import Ui
class APP(QObject):

    def __init__(self):
        super().__init__()
        self.creat_folder()
        self.ui = Ui()
        self.Q1 = Queue()  #open_capture
        self.Q2 = Queue()
        self.p = Process(target=process_, args=(self.Q1, self.Q2))
        self.p.daemon = True
        self.open_capture = OpenCapture(self.Q1, self.Q2)
        self.open_capture.emit_img.connect(self.set_normal_img)
        self.ui.btn1.clicked.connect(self.open_eye)
        self.ui.btn2.clicked.connect(self.open_normal)
        self.ui.btn3.clicked.connect(self.open)

    def creat_folder(self):
        if not os.path.exists("img_information"):  #判断是否存在文件夹如果不存在则创建文件夹
            os.makedirs("img_information")

    @pyqtSlot(QImage)
    def set_normal_img(self, image):
        self.ui.qlabel.setPixmap(QPixmap.fromImage(image))

#开启眨眼识别

    def open_eye(self):
        if self.ui.btn2.isChecked():
            self.ui.btn2.setChecked(False)
            if self.open_capture.isRunning():
                self.open_capture.timer3.stop()
                while self.Q1.qsize() != 0:  #清空队列
                    pass
                while self.Q2.qsize() != 0:
                    self.Q2.get()
            if self.ui.btn1.isChecked(): 
                if self.open_capture.isRunning():
                    self.open_capture.timer1.start(200)
        else:     
            if self.ui.btn1.isChecked():
                if self.open_capture.isRunning():
                     if psutil.Process(self.p.pid).status() == "stopped":
                        psutil.Process(self.p.pid).resume()
                        self.open_capture.timer1.start(200)
                        return 
                     self.open_capture.timer1.start(200)          
        if  ((self.ui.btn1.isChecked() is False) and (self.ui.btn2.isChecked()is False)):
                
                while self.open_capture.timer1.isActive():
                    self.open_capture.timer1.stop()
                while self.open_capture.timer2.isActive():
                    self.open_capture.timer2.stop()
                while self.open_capture.timer1.isActive():
                    self.open_capture.timer1.stop()
                while self.open_capture.timer2.isActive():
                    self.open_capture.timer2.stop()
                while self.Q1.qsize() != 0:  #清空队列
                    pass
                while self.Q2.qsize() != 0:
                    self.Q2.get()
                if self.open_capture.isRunning():                 
                    psutil.Process(self.p.pid).suspend()  #挂起进程
                
    def open_normal(self):
        if self.ui.btn1.isChecked():
            self.ui.btn1.setChecked(False)
            if self.open_capture.isRunning():
                while self.open_capture.timer1.isActive():
                    self.open_capture.timer1.stop()
                while self.open_capture.timer2.isActive():
                    self.open_capture.timer2.stop()
                while self.open_capture.timer1.isActive():
                    self.open_capture.timer1.stop()
                while self.open_capture.timer2.isActive():
                    self.open_capture.timer2.stop()
                while self.Q1.qsize() != 0:  #清空队列
                    pass
                while self.Q2.qsize() != 0:
                    self.Q2.get()
            if self.ui.btn2.isChecked():
                if self.open_capture.isRunning():
                    self.open_capture.timer3.start(1000)    
        else:        
            if self.ui.btn2.isChecked():
                if self.open_capture.isRunning():
                     if psutil.Process(self.p.pid).status() == "stopped":
                        psutil.Process(self.p.pid).resume()
                        self.open_capture.timer3.start(1000)
                        return 
                     self.open_capture.timer3.start(1000)

        if  ((self.ui.btn1.isChecked() is False) and (self.ui.btn2.isChecked()is False)):
                self.open_capture.timer3.stop()
                while self.Q1.qsize() != 0:  #清空队列
                    pass
                while self.Q2.qsize() != 0:
                    self.Q2.get()
                if self.open_capture.isRunning():                    
                    psutil.Process(self.p.pid).suspend()  #挂起进程
    def open(self):
        self.ui.btn3.clicked.disconnect(self.open)
        self.ui.btn3.clicked.connect(self.close)
        self.ui.btn3.setText("关闭摄像头")
        self.open_capture.start()
        if not self.p.is_alive():
            self.p.start()
        else:
            psutil.Process(self.p.pid).resume()  #恢复子进程
        if self.ui.btn1.isChecked():
            self.open_capture.timer1.start(200)
        if self.ui.btn2.isChecked():
            self.open_capture.timer3.start(1000)               
    def close(self):
       
        self.ui.btn3.clicked.connect(self.open)
        self.ui.btn3.clicked.disconnect(self.close)
        self.ui.btn3.setText("打开摄像头")
        self.open_capture.close()  #关闭摄像头
        self.open_capture.terminate()  #关闭线程
        self.open_capture.wait()
        while self.open_capture.timer3.isActive():
            self.open_capture.timer3.stop()

        while self.open_capture.timer1.isActive():
            self.open_capture.timer1.stop()
        while self.open_capture.timer2.isActive():
            self.open_capture.timer2.stop()
        while self.open_capture.timer1.isActive():
            self.open_capture.timer1.stop()
        while self.open_capture.timer2.isActive():
            self.open_capture.timer2.stop()            
        while self.Q1.qsize() != 0:  #清空队列
            pass
        while self.Q2.qsize() != 0:
            self.Q2.get()
        psutil.Process(self.p.pid).suspend()  #挂起进程
        self.ui.qlabel.clear()
        time.sleep(0.5)
        self.ui.qlabel.clear()


    
    def closeEvent(self, event): #关闭线程
        self.open_capture.terminate()
        self.open_capture.wait()
        self.open_capture.close()        
      
if __name__ == '__main__':

    app = QApplication(sys.argv)
    ex = APP()
    ex.ui.show()
    app.exec()
