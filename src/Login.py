import sys
from PyQt5.QtWidgets import QApplication, QWidget, QDialog, QLabel, QLineEdit, QPushButton, \
    QGridLayout, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt5.QtCore import pyqtSignal
from src.Studentdb import StudentDb
from src.MyMd5 import MyMd5
class LoginUi(QWidget):
    emitsingal  = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.resize(400, 300)

        self.user_label = QLabel('Username:', self)
        self.pwd_label = QLabel('Password:', self)
        self.user_line = QLineEdit(self)
        self.pwd_line = QLineEdit(self)
        self.login_button = QPushButton('Log in', self)
        self.signin_button = QPushButton('Sign in', self)

        #self.grid_layout = QGridLayout()
        self.h_user_layout = QHBoxLayout()
        self.h_password_layout = QHBoxLayout()
        self.h_in_layout = QHBoxLayout()
        
        self.v_layout = QVBoxLayout()

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()
        self.signin_page = SigninPage()     # 实例化SigninPage()

    def layout_init(self):
        self.h_user_layout.addWidget(self.user_label)
        self.h_user_layout.addWidget(self.user_line)
        self.h_password_layout.addWidget(self.pwd_label)
        self.h_password_layout.addWidget(self.pwd_line)
        self.h_in_layout.addWidget(self.login_button)
        self.h_in_layout.addWidget(self.signin_button)


        self.v_layout.addLayout(self.h_user_layout)
        self.v_layout.addLayout(self.h_password_layout)
        self.v_layout.addLayout(self.h_in_layout)


        self.setLayout(self.v_layout)

    def lineedit_init(self):
        self.user_line.setPlaceholderText('Please enter your usernumber')
        self.pwd_line.setPlaceholderText('Please enter your password')
        self.pwd_line.setEchoMode(QLineEdit.Password)

        self.user_line.textChanged.connect(self.check_input_func)
        self.pwd_line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.login_button.setEnabled(False)
        self.login_button.clicked.connect(self.check_login_func)
        self.signin_button.clicked.connect(self.show_signin_page_func)

    def check_login_func(self):
        student = StudentDb()
        def clear():
           self.pwd_line.clear()
           self.user_line.clear()
        
        if not self.user_line.text().isdigit():
            QMessageBox.critical(self, 'Wrong', 'Wrong Username or Password!') 
            clear()
            return 
        
        elif len (self.pwd_line.text()) < 6 or len (self.pwd_line.text())>13 :
            QMessageBox.critical(self, 'Wrong', 'Wrong Username or Password!') 
            clear()
            return 
        else:
            user_name = int(self.user_line.text())
            item = student.c.execute("select id_number,salt, password  from admin where id_number = {} ".format(user_name)).fetchall()[0]
            if len(item) != 1:
                password  = self.pwd_line.text()
                pass_word = MyMd5().create_md5(password,item[1])
                if pass_word == item[2]:
                   self.emitsingal.emit()
                else: 
                    QMessageBox.critical(self, 'Wrong', 'Wrong Username or Password!')    
                    clear()
                    return 
            else:QMessageBox.critical(self, 'Wrong', 'This User not exits')

       

       
    def show_signin_page_func(self):
        #self.signin_page.show()
        self.signin_page.exec_()

    def check_input_func(self):
        if self.user_line.text() and self.pwd_line.text():
            self.login_button.setEnabled(True)
        else:
            self.login_button.setEnabled(False)
    def closeEvent(self, event) :
        #self.emitsingal.emit() 
        pass

class SigninPage(QDialog):
    def __init__(self):
        super(SigninPage, self).__init__()
        self.signin_user_label = QLabel('Username:', self)
        self.signin_pwd_label = QLabel('Password:', self)
        self.signin_pwd2_label = QLabel('Password:', self)
        self.signin_user_line = QLineEdit(self)
        self.signin_pwd_line = QLineEdit(self)
        self.signin_pwd2_line = QLineEdit(self)
        self.signin_button = QPushButton('Sign in', self)

        self.user_h_layout = QHBoxLayout()
        self.pwd_h_layout = QHBoxLayout()
        self.pwd2_h_layout = QHBoxLayout()
        self.all_v_layout = QVBoxLayout()
        self.resize(300,200)

        self.lineedit_init()
        self.pushbutton_init()
        self.layout_init()

    def layout_init(self):
        self.user_h_layout.addWidget(self.signin_user_label)
        self.user_h_layout.addWidget(self.signin_user_line)
        self.pwd_h_layout.addWidget(self.signin_pwd_label)
        self.pwd_h_layout.addWidget(self.signin_pwd_line)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_label)
        self.pwd2_h_layout.addWidget(self.signin_pwd2_line)

        self.all_v_layout.addLayout(self.user_h_layout)
        self.all_v_layout.addLayout(self.pwd_h_layout)
        self.all_v_layout.addLayout(self.pwd2_h_layout)
        self.all_v_layout.addWidget(self.signin_button)

        self.setLayout(self.all_v_layout)

    def lineedit_init(self):
        self.signin_pwd_line.setEchoMode(QLineEdit.Password)
        self.signin_pwd2_line.setEchoMode(QLineEdit.Password)

        self.signin_user_line.textChanged.connect(self.check_input_func)
        self.signin_pwd_line.textChanged.connect(self.check_input_func)
        self.signin_pwd2_line.textChanged.connect(self.check_input_func)

    def pushbutton_init(self):
        self.signin_button.setEnabled(False)
        self.signin_button.clicked.connect(self.check_signin_func)

    def check_input_func(self):
        if self.signin_user_line.text() and self.signin_pwd_line.text() and self.signin_pwd2_line.text():
            self.signin_button.setEnabled(True)
        else:
            self.signin_button.setEnabled(False)

    def check_signin_func(self):
        student = StudentDb()
        def clear():
            self.signin_user_line.clear()
            self.signin_pwd_line.clear()
            self.signin_pwd2_line.clear()

        if not self.signin_user_line.text().isdigit():
           
            QMessageBox.critical(self, 'Wrong', 'Usernumber is only digit!')
            clear()
            return 
        elif self.signin_pwd_line.text() != self.signin_pwd2_line.text():
            QMessageBox.critical(self, 'Wrong', 'Two Passwords Typed Are Not Same!')
            clear()
            return 
        
        
        elif len (self.signin_pwd_line.text()) <6 or len (self.signin_pwd_line.text())>13 :
            QMessageBox.critical(self, 'Wrong', ' Passwords is too short!')
            clear()
            return 
        else:
            user_name = self.signin_user_line.text()
            user = student.c.execute("select id_number from admin where id_number = {} ".format(user_name)).fetchall()
            if len(user) == 1:
               QMessageBox.critical(self, 'Wrong', 'This Username Has Been Registered!')
               clear()
               return 
            else:
                
                user_name = int(self.signin_user_line.text())
                pass_word = self.signin_pwd_line.text()
                salt = MyMd5().create_salt()
                pass_word = MyMd5().create_md5(pass_word,salt)

                student.c.execute("INSERT INTO admin (id_number,password,salt) \
      VALUES (?, ?,?)",(user_name,pass_word,salt))
                QMessageBox.information(self, 'Information', 'Register Successfully')
                student.conn.commit()
                student.conn.close()
                self.close

                
       
