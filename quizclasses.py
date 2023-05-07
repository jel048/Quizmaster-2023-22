class Question:
    
    def __init__(self, questionid, idquiz, question, alt1, alt2, alt3):
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
        
        
        
class UserAnswers: #Fikses mot ny database
    def __init__(self, quizzee, quiznavn, question, answer):
        self.quizzee = quizzee
        self.quiznavn = quiznavn
        self.question = question
        self.answer = answer