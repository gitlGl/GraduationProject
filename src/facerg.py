from src.Face import Face
from threading import Timer
import numpy as np


from src.GlobalVariable import flag


class FaceRg():

    def __init__(self):
        self.face_data = np.random.random(128).astype('float32')
        self.face_obj = Face()
        self.refreshthread = Timer(10, self.reset).start()
        self.a = timerexec(self.refreshthread)
        self.former_result = ""
   
    def rg(self, img, rgbImage, raw_face,share):
        face_data = self.face_obj.encodeface(rgbImage, raw_face)
        flag = self.face_obj.compare_faces(face_data, self.face_data, axis=0)
        if flag < share.value:
            return self.former_result
        else:
            result, flag1 = self.face_obj.rg_face(img, face_data,share.value)
            if flag1:
                self.face_data = face_data
                self.former_result = result
                return result
            else:
                return result

    #每一段时间重置face_data值
    def reset(self):
        self.face_data = np.random.random(128).astype('float32')
      
        if  flag.gflag == 1:
            Timer(10, self.reset).start()

##用于退出定时器线程
class timerexec():

    def __init__(self, thandle):
        self.threadhandle = thandle

    def __del__(self):
        flag.gflag = 0
        self.threadhandle.cancel()
