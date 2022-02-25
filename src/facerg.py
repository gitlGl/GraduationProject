from src.face import Face
from threading import Timer
import numpy as np


gflag = 1  #用于定时器退出判断

class FaceRg():

    def __init__(self):
        self.face_data = np.random.random(128).astype('float32')
        self.face_obj = Face()
        self.refreshthread = Timer(10, self.reset).start()
        self.a = timerexec(self.refreshthread)

    def rg(self, img, rgbImage, raw_face):
        face_data = self.face_obj.encodeface(rgbImage, raw_face)
        flag = self.face_obj.compare_faces(face_data, self.face_data, axis=0)
        if flag < 0.4:
            return "同一个人"
        else:
            result, flag = self.face_obj.rg_face(img, face_data)
            if flag:
                self.face_data = face_data
                return result
            else:
                return result

    #每一段时间重置face_data值
    def reset(self):
        self.face_data = np.random.random(128).astype('float32')
        global gflag
        if gflag == 1:
            Timer(10, self.reset).start()

##用于退出定时器线程
class timerexec():

    def __init__(self, thandle):
        self.threadhandle = thandle

    def __del__(self):
        global gflag
        gflag = 0
        self.threadhandle.cancel()
