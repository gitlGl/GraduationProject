import xlrd
from PyQt5.QtWidgets import QFileDialog
from src import CreatUser
from PyQt5.QtWidgets import QApplication
import sys


class ReadStudentInformation():
    def __init__(self) -> None:

        pass
    def read_path(self):
        path ,_= QFileDialog.getOpenFileName(
                None, "选择文件", "c:\\", "files(*.xlsx )")
        print(path)        
        book = xlrd.open_workbook(path)
        sheets = book.sheets()
        for sheet in sheets:
            rows = sheet.nrows
            for i in range(1,rows):
                list1 =  sheet.row_values(rowx=i)
                print(list1)
                list2 = ["id_number","user_name","password","img_path" ]
                dic = dict(zip(list2,list1))
                print(dic)
                #CreatUser(dic)
        print("sucess")

if __name__ == '__main__':

    app = QApplication(sys.argv)
    test = ReadStudentInformation()
    test.read_path()   
    app.exec_()


                 
