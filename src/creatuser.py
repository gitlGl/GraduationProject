import random
from src.MyMd5 import MyMd5
from PyQt5.QtWidgets import QFileDialog
import face_recognition
import numpy as np
from src.Studentdb import StudentDb
import os, cv2
from src.GlobalVariable import models
class CreatUser():

    def __init__(self):
        pass

    def creat_user(self, id_number, user_name, password, img_path, vector,
                   salt):
        StudentDb().insert(id_number, user_name, password, img_path, vector,
                           salt)

    def get_img_path(self, id_number=123456):

        path = "img_information/{0}/log".format(str(id_number))
        if not os.path.exists(path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        return path

    def get_pass_word(self, salt, password="12345"):
        return MyMd5().create_md5(password, salt)

    def get_user_name(self, user_name="林"):
        return user_name

    def get_vector(self, id_number):
        """
        读取照片，获取人脸编码信息，把照片存储起来
        返回128维人脸编码信息
        """

        file_path, _ = QFileDialog.getOpenFileName(
            None, "选择图片", "c:\\", "Image files(*.jpg *.gif *.png)")
        img = cv2.imread(file_path)
        cv2.imwrite(
            "img_information/" + str(id_number) + "/" + str(id_number) +
            ".jpg", img)
        rgbImage = face_recognition.load_image_file(file_path)
        
        face = models.detector(rgbImage, 1)[0]
        frame = models.predictor(rgbImage, face)
        face_data = np.array(
            models.encoder.compute_face_descriptor(rgbImage,
                                                 frame,
                                                 num_jitters=1))
        face_data = np.ndarray.dumps(face_data)
        return face_data

    def get_id(self, id_number=12345):

        return random.randint(1, 20)