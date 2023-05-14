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
            result = self.cursor.fetchone()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    
    def createQuestion(self, idquiz, question, alt1, alt2, alt3):
        try:
            self.cursor.execute("INSERT INTO Qquestions\
                (idquiz, question, alt1, alt2, alt3) VALUES ((%s), (%s), (%s),(%s), (%s))", (idquiz, question, alt1, alt2, alt3))
        except mysql.connector.Error as err:
                print(err)
                
    def createQuestionEssay(self, idquiz, question):
        try:
            self.cursor.execute("INSERT INTO Qquestions\
                (idquiz, question) VALUES ((%s), (%s))", (idquiz, question))
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
    
    def questionsByQuiz(self, quizid):
        try:
            self.cursor.execute("SELECT questionid, idquiz, question, alt1, alt2, alt3 FROM Qquestions WHERE idquiz = (%s)", (quizid,))
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
                
                
    def getQuestion(self, id):
        try:
            self.cursor.execute("SELECT questionid, idquiz, question, alt1, alt2, alt3 FROM Qquestions WHERE questionid = (%s)", (id,))
            result = self.cursor.fetchone()
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
                    
    def showUserAnswers(self, idquiz, userID):
        try:
            self.cursor.execute("select userID, Qanswers.questionid, answer, godkjent, kommentar from Qanswers inner join Qquestions on \
                Qanswers.questionid = Qquestions.questionid WHERE idquiz = (%s) and userID = (%s)", (idquiz, userID))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def quizcomplete(self, userID, idquiz):
        try:
            self.cursor.execute("INSERT INTO Qquizcomplete (userID, idquiz) VALUES ((%s), (%s))", (userID, idquiz))
        except mysql.connector.Error as err:
                print(err)
    
    def showUserQuizes(self):
        try:
            self.cursor.execute("select Qquiz.quiznavn, Qquizcomplete.idquiz, Qquizcomplete.userID, Quser.Username, \
                Qquizcomplete.godkjent, Qquizcomplete.kommentar from ((Qquiz inner join Qquizcomplete on Qquiz.idquiz\
                    = Qquizcomplete.idquiz) inner join Quser on Qquizcomplete.userID = Quser.ID)")
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def commentQuiz(self, text, idquiz, userid):
        try:
            params = (text, idquiz, userid)
            sql = "UPDATE Qquizcomplete SET kommentar = %s WHERE idquiz = %s AND userID = %s"
            self.cursor.execute(sql, params)
        except mysql.connector.Error as err:
            print(err)
            
    def godkjennQuiz(self, userid, idquiz):
        try:
            params = (userid, idquiz)
            sql = "UPDATE Qquizcomplete SET godkjent = 1 WHERE userID = %s AND idquiz = %s"
            self.cursor.execute(sql, params)
        except mysql.connector.Error as err:
            print(err)
    
    def commentQuestion(self, text, questionid, userid):
        try:
            params = (text, questionid, userid)
            sql = "UPDATE Qanswers SET kommentar = %s WHERE questionid = %s AND userID = %s"
            self.cursor.execute(sql, params)
        except mysql.connector.Error as err:
            print(err)
            
    def godkjennSpm(self, userid, questionid):
        try:
            params = (userid, questionid)
            sql = "UPDATE Qanswers SET godkjent = 1 WHERE userID = %s AND questionid = %s"
            self.cursor.execute(sql, params)
        except mysql.connector.Error as err:
            print(err)
            
    def getQuizesMyResults(self, userID): #Viser brukerens godkjente resultater
        try:
            self.cursor.execute("Select Qquizcomplete.idquiz, Qquiz.quiznavn, userID, godkjent, kommentar from Qquizcomplete\
                inner join Qquiz on Qquizcomplete.idquiz = Qquiz.idquiz WHERE godkjent = 1 AND userID = (%s)", (userID,))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def getQuestionsMyResults(self, userID, quizid):
        try:
            self.cursor.execute("select userID, Qanswers.questionid, Qquestions.question, godkjent, answer, kommentar FROM Qanswers INNER JOIN \
                Qquestions ON Qanswers.questionid = Qquestions.questionid WHERE Qquestions.idquiz = (%s)  AND userID = (%s)", (quizid, userID))
            result = self.cursor.fetchall()
        except mysql.connector.Error as err:
                print(err)
        return result
    
    def deleteAnsweredQuiz(self, userid, quizid):
        try:
            self.cursor.execute("DELETE from Qquizcomplete where userID = (%s) and idquiz = (%s)", (userid, quizid))
        except mysql.connector.Error as err:
                    print(err)
                    
    def deleteQuestionsFromQuiz(self, userid, quizid):
        try:
            self.cursor.execute("DELETE Qanswers from Qanswers inner join Qquestions on Qanswers.questionid = Qquestions.questionid\
                where userID = (%s) and idquiz = (%s)", (userid, quizid))
        except mysql.connector.Error as err:
                    print(err)
                    
    def deleteAnsweredQuestion(self, userid, questionid):
        try:
            self.cursor.execute("DELETE from Qanswers where userID = (%s) and idquiz = (%s)", (userid, questionid))
        except mysql.connector.Error as err:
                    print(err)