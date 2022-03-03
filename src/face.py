import dlib
import numpy as np
from src.Studentdb import StudentDb
from src.Log import Log
from src.GlobalVariable import models

class Face():

    def __init__(self):
        pass
    #为人脸编码
    def encodeface(self, rgbImage, raw_face):
        return np.array(
            models.encoder.compute_face_descriptor(rgbImage, raw_face))

    #计算人脸相似度，flaot值越小越相似
    def compare_faces(self, face_encoding, test_encoding, axis=0):
        return np.linalg.norm(face_encoding - test_encoding, axis=axis)

    #与数据库人脸对比，相似度小于0.5则认为是同一个人
    def rg_face(self, img, face_data,distance):

        student = StudentDb()
        list = []
        for i in student.select("vector"):
            i = np.loads(i[0])
            list.append(i)
        if len(list) == 0:
            return "请先注册用户",False  
        distances = self.compare_faces(np.array(list), face_data, axis=1)
        min_distance = np.argmin(distances)
        print(distances[min_distance])
        if distances[min_distance] < distance:
            tembyte = np.ndarray.dumps(list[min_distance])
            student.conn.close()
            log = Log(tembyte)
            log.insert_time()
            log.insert_img(img)
            log.insert_cout()
            log.student.conn.close()
            return "验证成功：" + log.item[1], True
        else:
            return "验证失败", False
