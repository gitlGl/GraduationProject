import cv2, dlib
from src.facerg import FaceRg
import numpy as np
import time
from src.models import models 

#此用于面部特征计算进程
def process_(Q1, Q2):
    face_rg = FaceRg()

    while True:
        while not Q1.empty():
            img = Q1.get()
            rgbImage = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            gray = cv2.cvtColor(rgbImage, cv2.COLOR_RGB2GRAY)
            location_faces = models.detector(gray)
            if len(location_faces) == 1:
                raw_face = models.predictor(gray, location_faces[0])
                result = face_rg.rg(img, rgbImage, raw_face)
                Q2.put(result)
        time.sleep(1)