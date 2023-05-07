import mysql.connector


class MyDb:

    def __init__(self) -> None:
        dbconfig = {'host': 'kark.uit.no',
                    'user': 'stud_v23_jel048',
                    'password': 'jel048',
                    'database': 'stud_v23_jel048' }
        self.configuration = dbconfig
        

    def __enter__(self):
        self.conn = mysql.connector.connect(**self.configuration)
        self.cursor = self.conn.cursor()
        return self
#
    def __exit__(self, exc_type, exc_val, exc_trace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def query(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
    
    
    def visQuizer(self):
        try:
            self.cursor.execute("SELECT * FROM Qquiz")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def visQuizSpm(self, idquiz):
        try:
            self.cursor.execute("SELECT questionid, idquiz, question, alt1, alt2, alt3 FROM Qquestions WHERE idquiz = (%s)", (idquiz,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def getQuizId(self, quiznavn):
        try:
            self.cursor.execute("SELECT idquiz FROM Qquiz WHERE quiznavn = (%s)", (quiznavn,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    
    def createQuestion(self, idquiz, question, alt1, alt2, alt3):
        try:
            self.cursor.execute("INSERT INTO Qquestions\
                (idquiz, question, alt1, alt2, alt3) VALUES ((%s), (%s), (%s),(%s), (%s))", (idquiz, question, alt1, alt2, alt3))
        except mysql.connector.Error as err:
                print(err)
        
    def createQuiz(self, quiznavn, kategori):
        try:
            self.cursor.execute("INSERT INTO Qquiz\
                (quiznavn, quizkategori) VALUES ((%s), (%s))", (quiznavn, kategori))
        except mysql.connector.Error as err:
                print(err)
                
    def showCategories(self):
        try:
            self.cursor.execute("SELECT DISTINCT(quizkategori) FROM Qquiz")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def showQuizByCategory(self, kategori):
        try:
            self.cursor.execute("SELECT quiznavn FROM Qquiz WHERE quizkategori = (%s)", (kategori,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def questionsByQuiz(self, quiz):
        try:
            self.cursor.execute("SELECT questionid, idquiz, question, alt1, alt2, alt3 FROM Qquestions WHERE idquiz = (%s)", (quiz,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def userAnswer(self, userID, questionid, answer):
        try:
            self.cursor.execute("INSERT INTO Qanswers\
                (userID, questionid, answer) VALUES ((%s), (%s), (%s))", (userID, questionid, answer))
        except mysql.connector.Error as err:
                print(err)
                
                
    def getQuestions(self, id):
        try:
            self.cursor.execute("SELECT questionid, idquiz, question, alt1, alt2, alt3 FROM Qquestions WHERE idquiz = (%s)", (id,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def updateQuestion(self, question):
                
                try:
                    sql = '''UPDATE Qquestions
                    SET
                    question = %s, alt1 = %s, alt2 = %s, alt3 = %s
                    WHERE
                    questionid = %s'''
                    self.cursor.execute(sql, question)
                except mysql.connector.Error as err:
                    print(err)
                    
    def deleteQuestion(self, id):
        try:
            self.cursor.execute("DELETE FROM Qquestions WHERE questionid = (%s)", (id,))
        except mysql.connector.Error as err:
                    print(err)
                    
    def showUserAnswers(self, userID):
        try:
            self.cursor.execute("SELECT userID, questionid, answer FROM Qanswers WHERE userID = (%s)", (userID,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    