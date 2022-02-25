import cv2, copy
from PyQt6.QtCore import QThread, QTimer
import numpy as np
from PyQt6.QtGui import QImage
import dlib
from multiprocessing import Process, Queue
from multiprocessing import Process, Queue
from src.Process import *
from PyQt6.QtCore import pyqtSignal
#from PIL import Image, ImageDraw, ImageFont
from src.eyeblink import EyeBlink
from src.models import models

class OpenCapture(QThread):
    """
   用于启动普通识别模式
    """
    emit_img = pyqtSignal(QImage)

    def __init__(self, Q1, Q2):
        super().__init__()

        self.list_img = []
        self.check_eye = EyeBlink()
        self.timer1 = QTimer()
        self.timer1.timeout.connect(self.collect_frame)
        self.timer2 = QTimer()
        self.timer2.timeout.connect(self.get_result)
        self.timer3 = QTimer()
        self.timer3.timeout.connect(self.to_put)
        self.Q1 = Q1
        self.Q2 = Q2
        self.frame = np.random.randint(255, size=(900, 800, 3),
                                       dtype=np.uint8)  #初始化
        self.detector = dlib.get_frontal_face_detector()

    def run(self):
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        while True:
            ret, frame = self.cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.frame = frame
                #rgbImage = put_chines_test(frame,"请眨眼")
                p = convertToQtFormat(rgbImage)
                self.emit_img.emit(p)

    def to_put(self):
        #print("test")
        self.timer3.stop()
        #控制队列数量为1
        if self.Q1.qsize() == 0:
            self.Q1.put(self.frame)
        if not self.Q2.empty():
            print(self.Q2.get())

        self.timer3.start(2000)

    def collect_frame(self):
        self.timer1.stop()
        if len(self.list_img) <= 1:
            self.list_img.append(self.frame)
        elif len(self.list_img) == 2:
            list_img = copy.deepcopy(self.list_img)
            flag = self.check_eye.compare2faces(list_img)
            if flag:
                self.Q1.put(self.list_img[0])
                self.timer2.start(1000)
                self.list_img.clear()
                return
            print(flag)
            self.list_img.clear()
        self.timer1.start(200)

    def get_result(self):
        self.timer2.stop()
        if self.Q2.qsize != 0:
            result = self.Q2.get()
            print(result)
            self.timer1.start(200)
        else:
            self.timer2.start(1000)

    def close(self):
        self.cap.release()
        cv2.destroyAllWindows()


#转换位qt图像格式
def convertToQtFormat(frame_show):
    h, w, ch = frame_show.shape
    bytesPerLine = ch * w
    convertToQtFormat = QImage(frame_show.data, w, h, bytesPerLine,
                               QImage.Format.Format_RGB888)
    p = convertToQtFormat.scaled(480, 600)
    return p


#为图片渲染中文
def put_chines_test(frame, chinnes_text):
    rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    location = models.detector(rgbImage)
    if len(location) == 1:
        location = location[0]
        font = ImageFont.truetype("./resources/simsun.ttc",
                                  50,
                                  encoding="utf-8")
        rgbImage = Image.fromarray(rgbImage)
        draw = ImageDraw.Draw(rgbImage)
        draw.text(((location.right() + 6, location.top() - 6)), chinnes_text,
                  (0, 0, 255), font)
        rgbImage = np.asarray(rgbImage)
    return rgbImage