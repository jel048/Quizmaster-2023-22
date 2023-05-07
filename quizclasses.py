class Question:
    
    def __init__(self, id, question, alt1, alt2, alt3, correct, quiznavn):
        self.id = id
        self.question = question
        self.alt1 = alt1
        self.alt2 = alt2
        self.alt3 = alt3
        self.correct = correct
        self.quiznavn = quiznavn
        
        
class Quiz:
    
    def __init__(self, Quiznavn, quizKategori):
        self.Quiznavn = Quiznavn
        self.quizKategori = quizKategori
        
        
class Score:
    def __init__(self, quizzee, quiznavn, score):
        self.quizzee = quizzee
        self.quiznavn = quiznavn
        self.score = score
        
class UserAnswers:
    def __init__(self, quizzee, quiznavn, question, answer):
        self.quizzee = quizzee
        self.quiznavn = quiznavn
        self.question = question
        self.answer = answer