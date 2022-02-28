
from turtle import distance
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QPushButton, QVBoxLayout, QHBoxLayout
from src.Process import *
from PyQt5.QtWidgets import QSlider
from PyQt5.QtCore import pyqtSlot,QTimer,Qt
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import multiprocessing
class Ui(QWidget):
    def __init__(self,thread):
        super().__init__()
        self.thread = thread
        self.share = multiprocessing.Value("f",0.4)

        self.thread.emit_result.connect(self.show_result)
        self.timer = QTimer()
        self.timer.timeout.connect(self.clear_qlabel2)
        
        self.setFixedSize(480, 600)
        #self.setStyleSheet ("border:2px groove gray;border-radius:10px;padding:2px 2px;")
        self.groupbox_1 = QGroupBox( self)                       # 1
        self.groupbox_2 = QGroupBox( self)
        self.groupbox_1.setFixedSize(460,35)
        self.groupbox_2.setFixedSize(460,35)
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
        self.btn1.setFixedSize(100,20)
        self.btn2.setFixedSize(100,20)
        self.qlabel1 = QLabel()
        self.qlabel2 = QLabel()
        self.qlabel3 = QLabel()
        self.qlabel3.setFixedSize(30,20)
        self.qlabel3.setFont(QFont("Arial",10))
        self.qlabel3.setAlignment(Qt.AlignCenter)
        self.qlabel3.setText("0.4")
        self.slider =  QSlider(Qt.Horizontal)
        self.slider.setTickPosition(QSlider.TicksBelow)
        self.slider.setMaximum(12)
        self.slider.setMinimum(0)
        self.slider.setSingleStep(1)
        self.slider.setValue(8)
        self.slider.setTickInterval(1)
        self.slider.valueChanged.connect(self.valueChange)

        #self.slider.setTickPosition()
        
        self.slider.setFixedSize(100,20)
        #self.slider.move(360)
        self.slider.height()
        #self.btn3.setStyleSheet("border:2px groove gray;border-radius:10px;padding:2px 2px;background-color: yellow")
        self.qlabel = QLabel()
        self.btn3.setFixedSize(200,20)
        Hlayout.addWidget(self.btn2)
        Hlayout.addWidget(self.btn1)
        Hlayout.addWidget(self.btn3)
        self.groupbox_1.setLayout(Hlayout)
        Hlayout2.addWidget(self.qlabel1)
        Hlayout2.addWidget(self.qlabel2)
        Hlayout2.addWidget(self.slider)
        Hlayout2.addWidget(self.qlabel3)
        self.groupbox_2.setLayout(Hlayout2)
        
        #Vlayout.addLayout(Hlayout)
        Vlayout.addWidget(self.groupbox_1)
        #Vlayout.addLayout(Hlayout2)
        Vlayout.addWidget(self.groupbox_2)
      
        Vlayout.addWidget(self.qlabel)

        allvlaout.addLayout(Vlayout)
        self.setLayout(allvlaout)
  
        self.setWindowTitle("测试")
    def closeEvent(self, event): #关闭线程
        self.thread.terminate()
        self.thread.wait()
        if hasattr(self.thread,"cap"):
            self.thread.close()
    @pyqtSlot(str)          
    def show_result(self,str_result):
        self.qlabel2.setText(str_result)
        self.timer.start(3000)
    def clear_qlabel2(self):
        self.timer.stop()
        self.qlabel2.clear()
    def valueChange(self):
        distance = round(self.slider.value()*0.05,2)
        self.share.value = distance
        self.qlabel3.setText(str(distance))

        