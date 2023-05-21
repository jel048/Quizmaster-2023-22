import mysql.connector
from mysql.connector import errorcode
from werkzeug.security import generate_password_hash, check_password_hash

class UserReg:

    def __init__(self) -> None:

        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v23_jel048',
                    'password': 'jel048',
                    'database': 'stud_v23_jel048' }

        self.configuration = dbconfig

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor(prepared=True)
        return self

    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def getUser(self, username):
        try:
            self.cursor.execute("SELECT * FROM Quser WHERE  username=(%s)", (username,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result

    def getUserById(self, id):
        try:
            self.cursor.execute("SELECT * FROM Quser WHERE  id=(%s)", (id,))
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def registerUser(self, username, password, isAdmin):
        passwordhash = generate_password_hash(password)
        try:
            self.cursor.execute("INSERT INTO Quser VALUES ((%s), (%s), (%s))", (username, passwordhash, isAdmin))
        except mysql.connector.Error as err:
                print(err)
                
                
      