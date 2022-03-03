from .Studentdb import StudentDb
import datetime
import cv2
import os

class Log():

    def __init__(self, vector):
        self.student = StudentDb()
        self.item = self.get_item(vector)

    def insert_time(self):
        """
        向数据库插入识别时间
        """
        StyleTime = self.get_time()
        list = self.item # 用户信息
        if list[5] == None:
            self.student.update("date_time", StyleTime, list[0])
        else:
            string = list[5] + StyleTime
            self.student.update("date_time", string, list[0])

    def insert_img(self, img):
        """
        向数据库插入识时照片
        """
        path = self.item[3]
        if not os.path.exists(path):  #判断是否存在文件夹如果不存在则创建为文件夹
            os.makedirs(path)
        cv2.imwrite(
            path + "/" + self.get_time().replace(":", "-") + ".jpg",
            img)

    def get_item(self, vector):
        return self.student.select("vector", vector).fetchall()[0]#取出返回所有数据，fetchall返回类型是[()]

    def get_time(self):
        return str(datetime.datetime.now().strftime("%Y-%m-%d-%H:%M:%S "))
    
    def insert_cout(self):
        if self.item[7] == None:
            cout  = 1
            self.student.update("cout",cout,self.item[0])
        else:
            cout = self.item[7] + 1
            self.student.update("cout",cout,self.item[0])    
