class Question:
    
    def __init__(self, questionid, idquiz, question, alt1 = 0, alt2 = 0, alt3 = 0):
        self.id = questionid
        self.idquiz = idquiz
        self.question = question
        self.alt1 = alt1
        self.alt2 = alt2
        self.alt3 = alt3
        
        
class Quiz: #Fikses mot ny database
    
    def __init__(self, Quiznavn, quizKategori):
        self.Quiznavn = Quiznavn
        self.quizKategori = quizKategori
        
        
        
class UserAnswers:
    def __init__(self, userID, questionid, answer, godkjent, kommentar = None):
        self.userID = userID
        self.questionid = questionid
        self.answer = answer
        self.godkjent = "Godkjent" if godkjent == 1 else "Ikke Godkjent"
        self.kommentar = kommentar

class AnsweredQuizes:
    def __init__(self, quiznavn, idquiz, userID, Username, godkjent, kommentar = None):
        self.quiznavn = quiznavn
        self.idquiz = idquiz
        self.userID = userID
        self.Username = Username
        self.godkjent = "Godkjent" if godkjent == 1 else "Ikke Godkjent"
        self.kommentar = kommentar
        

class ApprovedQuizes:
    def __init__(self, idquiz, quiznavn, userID, godkjent, kommentar = None):
        self.idquiz = idquiz
        self.quiznavn = quiznavn
        self.userID = userID
        self.kommentar = kommentar
        self.godkjent = "Godkjent" if godkjent == 1 else "Ikke Godkjent"

class ApprovedQuestions:
    def __init__(self, userID, questionid, question, godkjent, answer, kommentar = None,):
        self.userID = userID
        self.questionid = questionid
        self.question = question
        self.kommentar = kommentar
        self.godkjent = "Godkjent" if godkjent == 1 else "Ikke Godkjent"
        self.answer = answer
        