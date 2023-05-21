from wtforms import Form, StringField, SubmitField, RadioField, validators
from wtforms.validators import DataRequired
from wtforms.fields import  HiddenField, TextAreaField


class CreateQuestionForm(Form):
    id = HiddenField()
    idquiz = HiddenField()
    question = StringField('Spørsmål', validators =[DataRequired()])
    alt1 = StringField('Alternativ 1', validators =[DataRequired()])
    alt2 = StringField('Alternativ 2', validators =[DataRequired()])
    alt3 = StringField('Alternativ 3', validators =[DataRequired()])
    submit = SubmitField('Send')

class CreateEssayQuestionForm(Form):
    id = HiddenField()
    idquiz = HiddenField()
    question = StringField('Spørsmål', validators =[DataRequired()])
    submit = SubmitField('Send')

class AnswerQuestionForm(Form): 
    answer = RadioField('Alternativ:', choices=[('alt1','description'),('alt2','whatever'),('alt3','whatever')]) #form.alternatives.choices = (question.alt1,question.alt1),(question.alt2,question.alt2),(question.alt3,question.alt3)
    submit = SubmitField('Neste')

class AnswerQuestionFormEssay(Form): 
    answer = TextAreaField('Svar', validators =[DataRequired()])
    submit = SubmitField('Neste')

    
class quizForm(Form):
    quiznavn = StringField('Quiznavn', validators =[DataRequired()])
    kategori = StringField('Kategori', validators =[DataRequired()])
    submit = SubmitField('Opprett quiz')
