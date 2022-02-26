
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from src.Process import *
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Ui(QWidget):
    def __init__(self,thread):
        super().__init__()
        self.thread = thread
        self.setFixedSize(480, 600)
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()
        Hlayout2 = QHBoxLayout()
        allvlaout = QVBoxLayout()

        self.btn2 = QCheckBox(self)
        self.btn1 = QCheckBox(self)
        self.btn1.setText("眨眼模式")
        self.btn2.setText("普通模式")
        self.btn3 = QPushButton()
        self.btn3.setText("打开摄像头")
        self.btn4 = QPushButton()
        self.btn1.setFixedSize(100,30)
        self.btn2.setFixedSize(100,30)
        
        self.btn3.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 2px;background-color: yellow")
        self.qlabel = QLabel()
        self.btn3.setFixedSize(200,20)
        Hlayout.addWidget(self.btn2)
        Hlayout.addWidget(self.btn1)
        Hlayout.addWidget(self.btn3)
        Vlayout.addLayout(Hlayout)
        Vlayout.addLayout(Hlayout2)
      
      
        Vlayout.addWidget(self.qlabel)

        allvlaout.addLayout(Vlayout)
        self.setLayout(allvlaout)
        
        self.setWindowTitle("测试")
    def closeEvent(self, event): #关闭线程
        self.thread.terminate()
        self.thread.wait()
        if hasattr(self.thread,"cap"):
            self.thread.close()   




