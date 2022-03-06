import random
from src.MyMd5 import MyMd5
from PyQt5.QtWidgets import QFileDialog
import face_recognition
import numpy as np
from src.Studentdb import StudentDb
import os, cv2
from src.GlobalVariable import models
import xlrd
from pathlib import Path
from PyQt5.QtCore import pyqtSignal
class CreatUser():
    def __init__(self):
        pass

    def get_pass_word(self, salt, password="12345"):
        return MyMd5().create_md5(password, salt)

    def get_vector(self, id_number,img_path = None ):
        """
        读取照片，获取人脸编码信息，把照片存储起来
        返回128维人脸编码信息
        """
        file_path = ""
        if img_path == None:
            file_path, _ = QFileDialog.getOpenFileName(
                None, "选择图片", "c:\\", "Image files(*.jpg *.gif *.png)")
        else: file_path =  img_path

        img = cv2.imread(file_path)
        if img is None:
            return
        cv2.imwrite(
            "img_information/" + str(id_number) + "/" + str(id_number) +
            ".jpg", img)
        rgbImage = face_recognition.load_image_file(file_path)
        face = models.detector(rgbImage, 1)[0]
        frame = models.predictor(rgbImage, face)
        face_data = np.array(
            models.encoder.compute_face_descriptor(rgbImage,frame))
        face_data = np.ndarray.dumps(face_data)
        return face_data

    
    
           

class CreatStudentUser(CreatUser):
    def __init__(self):
        super().__init__()
        self.creat_user()

    def creat_user(self):
        path ,_= QFileDialog.getOpenFileName(
                None, "选择文件", "c:\\", "files(*.xlsx )")
        if path == '':
            return
    
        book = xlrd.open_workbook(path)
        sheets = book.sheets()
        list_problem = []
        def error_string(row,column,error_information):
            return "第{0}行第{1}列: ".format(row,column) + str(error_information)
        for sheet in sheets:
            rows = sheet.nrows
            for i in range(1,rows):
                list1 =  sheet.row_values(rowx=i)
                if type(list1[0]) is str:
                    if list1[0].isdigit() and len(list1[0]) == 13:
                        list1[0] = int(list1[0])
                    else: 
                        list_problem.append(error_string(i,"1",list1[0]))
                        continue
                elif type(list1[0]) is float:
                    int_ = int(list1[0])
                    if  len(str(int_)) == 13:
                        list1[0] = int(list1[0])
                    else:   
                        list_problem.append(error_string(i,"1",int(list1[0])))
                        continue
                   
                list1[1] = str(list1[1])
                list1[2] = str(list1[2])

                list1[3] = str(list1[3])
                path =  Path(list1[3])
               
                if path.is_file():
                    pass
                else:
                    string = "第{0}行第4列: ".format(i)+str(list1[3])
                    list_problem.append(string)
                    continue

                list2 = ["id_number","user_name","password","img_path" ]
                dic = dict(zip(list2,list1))
                information =  self.set_information(dic)
                self.insert_user(information)
               
        for j in list_problem:        
            print("错误信息：",j)
    def set_information(self, part_information):
        information = {}
        information["user_name"] = part_information["user_name"]
        information['salt'] = MyMd5().create_salt()
        information["img_path"] = self.get_img_path(part_information["id_number"])
        information["id_number"] = part_information["id_number"]
        information["password"] = self.get_pass_word(part_information["password"],information["salt"])
        information["vector"] = self.get_vector(part_information["id_number"],part_information["img_path"])
        return information


    def insert_user(self,information):
        StudentDb().insert_user(information["id_number"], information["user_name"], information["password"], 
        information["img_path"], information["vector"],
                           information["salt"])


    def get_img_path(self, id_number = 123456):
        path = "img_information/{0}/log".format(str(id_number))
        if not os.path.exists(path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        return path