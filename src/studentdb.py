import sqlite3


class StudentDb():

    def __init__(self):
        self.conn = sqlite3.connect('./resources/company.db')
        self.c = self.conn.cursor()
        self.creatble()
    
    def creatble(self):
        self.c.execute('''CREATE TABLE IF NOT EXISTS student
       ( 
        id_number            INT     NOT NULL,
        user_name           CHAR(50)    NOT NULL,
        password        char(20)    NOT NULL,
        img_path        char(40),
        vector         blob       NOT NULL,
        date_time           text ,      
        salt              char(10)  NOT NULL ,
        cout              INT           );''')
        self.conn.commit()

    def insert(self, id_number, user_name, password, img_path, vector, salt):
        self.c.execute(
            "INSERT INTO student (id_number,user_name,password ,img_path ,vector,salt) \
      VALUES (?, ?, ? , ?,?,?)",
            (id_number, user_name, password, img_path, vector, salt))
        self.conn.commit()

    def delete(self, id):
        self.c.execute("delete from student where id_number = {0}".format(id))
        self.conn.commit()

    def update(self, item, update, id):
        self.c.execute(
            "UPDATE student SET {0} = ? WHERE id_number = ?".format(item),
            (update, id))
        self.conn.commit()

    def select(self, item, to_search=None):
        if to_search == None:
            return self.c.execute("SELECT {0} from student".format(item))
        else:
            return self.c.execute(
                "SELECT  * from student where {0} = ?".format(item),
                (to_search, ))
