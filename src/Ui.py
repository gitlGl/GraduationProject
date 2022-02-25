
from PyQt6.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from src.Process import *
from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSlot
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class Ui(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(480, 600)
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        Vlayout = QVBoxLayout()
        Hlayout = QHBoxLayout()
        Hlayout2 = QHBoxLayout()
        allvlaout = QVBoxLayout()

        self.btn1 = QCheckBox(self)
        self.btn2 = QCheckBox(self)
        self.btn3 = QPushButton()
        self.btn4 = QPushButton()
        self.btn1.setFixedSize(100,30)
        self.btn2.setFixedSize(100,30)
        
        self.btn3.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 2px;background-color: yellow")
        self.qlabel = QLabel()
        self.btn3.setFixedSize(200,20)
        Hlayout.addWidget(self.btn1)
        Hlayout.addWidget(self.btn2)
        Hlayout.addWidget(self.btn3)
        Vlayout.addLayout(Hlayout)
        Vlayout.addLayout(Hlayout2)
      
      
        Vlayout.addWidget(self.qlabel)

        allvlaout.addLayout(Vlayout)
        self.setLayout(allvlaout)
        self.btn1.setText("打开摄像头")
        self.btn2.setText("打开摄像头")
        
        self.setWindowTitle("测试")




