import cv2, numpy as np
from PyQt6.QtCore import QThread
import dlib
from scipy.spatial import distance as dist
from imutils import face_utils
from PyQt6.QtCore import pyqtSignal
from src.Process import *
from src.models import models

class EyeBlink(QThread):
    singal = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        models.detector = dlib.get_frontal_face_detector()  # 获取人脸模型
        self.img1 = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
        self.img2 = np.random.randint(255, size=(900, 800, 3), dtype=np.uint8)
        self.singal.connect(self.compare2faces)

        EYE_AR_THRESH = 0.3  #ear小于0.3时认为是闭眼状态

        #68个人脸特征中眼睛的位置

        self.lStart, self.lEnd = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        self.rStart, self.rEnd = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def eye_aspect_ratio(self, eye):
        """
        计算眼睛大小
        """
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])

        ear = (A + B) / (2.0 * C)  #眼睛大小值

        return ear

    def compare2faces(self, list_img):  #对比两张人脸照片对比是否发生眨眼

        gray1 = cv2.cvtColor(list_img[0], cv2.COLOR_RGB2GRAY)
        gray2 = cv2.cvtColor(list_img[1], cv2.COLOR_RGB2GRAY)
        rect1 = models.detector(gray1, 0)
        rect2 = models.detector(gray2, 0)
        list = []
        if (len(rect1) == 1) and (len(rect2)) == 1:
            list.append(self.comput_eye(gray1, rect1))
            list.append(self.comput_eye(gray2, rect2))
            result = abs(list[0] - list[1])
            if result >= 0.1:
                return True
        else:
            return False
        return False

    def comput_eye(self, gray, rect):
        shape = models.predictor(gray, rect[0])
        shape = face_utils.shape_to_np(shape)  #68个人脸特征坐标
        leftEye = shape[self.lStart:self.lEnd]
        rightEye = shape[self.rStart:self.rEnd]
        leftEAR = self.eye_aspect_ratio(leftEye)
        rightEAR = self.eye_aspect_ratio(rightEye)
        ear = (leftEAR + rightEAR) / 2.0  # 两个眼睛大小平均值
        return ear
