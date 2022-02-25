
from src.creatuser import CreatUser
from src.mymd5 import MyMd5
import sys
from PyQt6.QtWidgets import QApplication,QWidget


class test(QWidget):
    def __init__(self):
        super().__init__()
        self.create_user = CreatUser()
        self.id_number = self.create_user.get_id()
        self.user_name = self.create_user.get_user_name()
        self.img_path = self.create_user.get_img_path(self.id_number)
        self.salt = MyMd5().create_salt()
        self.password = self.create_user.get_pass_word(self.salt)
        self.vector = self.create_user.get_vector(self.id_number)
        self.create_user.creat_user(self.id_number,self.user_name,
        self.password,self.img_path,self.vector,self.salt)


if __name__ == '__main__':
  

    app = QApplication(sys.argv)
    
    test = test()
    
    
    app.exec()


